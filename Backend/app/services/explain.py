import numpy as np
from .model import _ensure_loaded, _model, _vectorize

def _score_margin(X: np.ndarray) -> float:
    if hasattr(_model, "decision_function"):
        return float(_model.decision_function(X)[0])
    if hasattr(_model, "predict_proba"):
        return float(_model.predict_proba(X)[0, 1])
    return float(getattr(_model, "predict", lambda x: [0])(X)[0])

def explain_local(features_vector=None, features_dict=None, top_k: int = 8):
    _ensure_loaded()
    X, names = _vectorize(features_vector, features_dict)

    base = _score_margin(X)
    delta = 1e-3
    vals = []
    for j in range(X.shape[1]):
        Xp = X.copy()
        Xp[0, j] += delta
        vals.append(_score_margin(Xp) - base)
    vals = np.array(vals, dtype=float)

    idx = np.argsort(-np.abs(vals))[:top_k]
    contribs = [
        {"feature": names[i], "value": float(X[0, i]), "contribution": float(vals[i])}
        for i in idx
    ]
    return {"base_value": float(base), "contributions": contribs, "top_k": int(top_k)}
