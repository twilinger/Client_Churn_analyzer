import os
import json
import typing as t
from ..utils.settings import settings

os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

# Import the expert class
from core.ollama_handle import OllamaChurnExpert 
try:
    from db.vector_db import VectorDB           
except Exception:
    VectorDB = None

_expert: OllamaChurnExpert | None = None
_vector_db: t.Any = None

def _ensure_loaded():
    global _expert, _vector_db
    if _expert is None:
        if VectorDB and settings.VECTOR_DB_PATH:
            _vector_db = VectorDB(path=settings.VECTOR_DB_PATH)
        _expert = OllamaChurnExpert(
            model=settings.OLLAMA_MODEL,
            host=settings.OLLAMA_HOST,
            vector_db=_vector_db,
            top_k=getattr(settings, "TOP_K", 4),
        )

def _to_features_dict(features_vector: list[float] | None,
                      features_dict: dict[str, t.Any] | None) -> dict[str, t.Any]:
    if features_dict is not None:
        return features_dict
    if features_vector is not None:
        return {f"f{i}": float(v) for i, v in enumerate(features_vector)}
    raise ValueError("Provide features_dict or features_vector")

def predict_proba(features_vector: list[float] | None = None,
                  features_dict: dict[str, t.Any] | None = None,
                  *, extra_context: str | None = None) -> float:
    """
    Predict churn probability using OllamaChurnExpert and return value 0..1.
    If expert has predict_proba method, use it directly,
    otherwise ask LLM for JSON with churn_proba field.
    """
    _ensure_loaded()
    feats = _to_features_dict(features_vector, features_dict)
    if hasattr(_expert, "predict_proba"):
        return float(_expert.predict_proba(features=feats, extra_context=extra_context))

    prompt = (
        "You are a churn scoring assistant.\n"
        "Return STRICT JSON ONLY: {\"churn_proba\": <float between 0 and 1>}.\n"
        f"Features: {json.dumps(feats, ensure_ascii=False)}\n"
    )
    if extra_context:
        prompt += f"\nContext:\n{extra_context}\n"

    if hasattr(_expert, "ask"):
        text = _expert.ask(prompt)
    elif hasattr(_expert, "chat"):
        text = _expert.chat(prompt)
    else:
        raise RuntimeError("OllamaChurnExpert has no .ask/.chat/.predict_proba")

    p = _extract_churn_proba(text)
    return max(0.0, min(1.0, p))

def explain_local(features_vector: list[float] | None = None,
                  features_dict: dict[str, t.Any] | None = None,
                  *, top_k: int = 8,
                  extra_context: str | None = None) -> dict:
    """
    Ask LLM for explanation. Returns structured response for API.
    """
    _ensure_loaded()
    feats = _to_features_dict(features_vector, features_dict)

    sys = (
        "You are a churn explainer. Return STRICT JSON ONLY with schema:\n"
        '{"base_value": number, "contributions":[{"feature": string, "value": number, "contribution": number}], "top_k": number, "reason": string}\n'
        "Contributions: signed effect (approx).\n"
        f"top_k: {top_k}\n"
    )
    user = f"Features: {json.dumps(feats, ensure_ascii=False)}"
    if extra_context:
        user += f"\nContext:\n{extra_context}"

    if hasattr(_expert, "ask_json"):
        obj = _expert.ask_json(system=sys, user=user)
    else:
        if hasattr(_expert, "ask"):
            text = _expert.ask({"system": sys, "user": user})
        else:
            text = _expert.chat({"system": sys, "user": user})
        obj = _extract_json(text)

    # sanity-check
    base = float(obj.get("base_value", 0.5))
    contribs = obj.get("contributions", [])
    if not isinstance(contribs, list):
        contribs = []
    contribs = contribs[:top_k]
    norm = []
    for c in contribs:
        try:
            norm.append({
                "feature": str(c.get("feature")),
                "value": float(c.get("value")) if c.get("value") is not None else None,
                "contribution": float(c.get("contribution")) if c.get("contribution") is not None else None,
            })
        except Exception:
            continue

    return {
        "base_value": base,
        "contributions": norm,
        "top_k": top_k,
        "reason": obj.get("reason"),
    }

import re
JSON_RE = re.compile(r"\{.*\}", re.S)

def _extract_json(text: str) -> dict:
    m = JSON_RE.search((text or "").strip())
    if not m:
        raise ValueError(f"Cannot find JSON in output: {text[:200]}...")
    return json.loads(m.group(0))

def _extract_churn_proba(text: str) -> float:
    obj = _extract_json(text)
    return float(obj.get("churn_proba"))
