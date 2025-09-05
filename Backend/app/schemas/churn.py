from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class ChurnRequest(BaseModel):
    features_dict: Optional[Dict[str, float]] = None
    features_vector: Optional[List[float]] = None
    extra_context: Optional[str] = None  
    
class ChurnResponse(BaseModel):
    churn_proba: float = Field(..., ge=0.0, le=1.0)

class ExplainItem(BaseModel):
    feature: str
    value: float | None = None
    contribution: float | None = None

class ExplainResponse(BaseModel):
    base_value: float | None = None
    contributions: List[ExplainItem] = []
    top_k: int = 0
    reason: str | None = None 
