from fastapi import APIRouter, HTTPException
from ..schemas.churn import ChurnRequest, ChurnResponse, ExplainResponse
from ..services.model import predict_proba, explain_local

router = APIRouter(prefix="/api/churn", tags=["churn"])

@router.post("/predict", response_model=ChurnResponse)
def predict(req: ChurnRequest):
    try:
        p = predict_proba(req.features_vector, req.features_dict, extra_context=req.extra_context)
        return {"churn_proba": p}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/explain", response_model=ExplainResponse)
def explain(req: ChurnRequest):
    try:
        res = explain_local(req.features_vector, req.features_dict, top_k=8, extra_context=req.extra_context)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# New endpoints for hotel operations
@router.get("/dashboard-stats")
def get_dashboard_stats():
    """Get dashboard statistics for hotel operations"""
    return {
        "total_customers": 1247,
        "churn_rate": 23.4,
        "ai_interactions": 3421,
        "satisfaction_score": 4.2,
        "high_risk_customers": 156,
        "avg_response_time": "1.2s"
    }

@router.get("/customer-segments")
def get_customer_segments():
    """Get customer segment distribution"""
    return {
        "segments": [
            {"name": "Business", "value": 35, "color": "#8884d8"},
            {"name": "Leisure", "value": 45, "color": "#82ca9d"},
            {"name": "VIP", "value": 20, "color": "#ffc658"}
        ]
    }

@router.get("/churn-trend")
def get_churn_trend():
    """Get churn rate trend over time"""
    return {
        "trend": [
            {"month": "Jan", "rate": 25.2},
            {"month": "Feb", "rate": 23.8},
            {"month": "Mar", "rate": 22.1},
            {"month": "Apr", "rate": 24.5},
            {"month": "May", "rate": 23.4},
            {"month": "Jun", "rate": 21.9}
        ]
    }