from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

# Создаем приложение
app = FastAPI(
    title="Hotel AI Suite",
    version="1.0.0",
    description="AI-powered hotel customer service platform"
)

# Добавляем CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники для тестирования
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простые модели данных
class ChatRequest(BaseModel):
    message: str
    context: str = "hotel_operations"

class ChatResponse(BaseModel):
    response: str
    processing_time: float

class ChurnRequest(BaseModel):
    features_vector: list[float] = None
    features_dict: dict = None
    extra_context: str = None

class ChurnResponse(BaseModel):
    churn_proba: float

# Основные endpoints
@app.get("/")
def read_root():
    return {
        "message": "🏨 Hotel AI Suite is running!", 
        "status": "success",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "chat": "/api/chat/message",
            "churn": "/api/churn/predict",
            "dashboard": "/api/churn/dashboard-stats"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "version": "1.0.0",
        "timestamp": time.time(),
        "message": "All systems operational"
    }

# Churn Analysis endpoints
@app.post("/api/churn/predict", response_model=ChurnResponse)
def predict_churn(req: ChurnRequest):
    """Простое предсказание churn"""
    churn_proba = 0.5  # Базовая вероятность
    
    if req.features_dict:
        if req.features_dict.get("contract") == "Month-to-month":
            churn_proba += 0.3
        if req.features_dict.get("payment_method") == "Electronic check":
            churn_proba += 0.2
        if req.features_dict.get("monthly_charges", 0) > 70:
            churn_proba += 0.1
        if req.features_dict.get("tenure", 0) < 12:
            churn_proba += 0.15
    
    return ChurnResponse(churn_proba=min(churn_proba, 1.0))

@app.get("/api/churn/dashboard-stats")
def get_dashboard_stats():
    """Статистика для дашборда"""
    return {
        "total_customers": 1247,
        "churn_rate": 23.4,
        "ai_interactions": 3421,
        "satisfaction_score": 4.2,
        "high_risk_customers": 156,
        "avg_response_time": "1.2s"
    }

@app.get("/api/churn/customer-segments")
def get_customer_segments():
    """Сегменты клиентов"""
    return {
        "segments": [
            {"name": "Business", "value": 35, "color": "#8884d8"},
            {"name": "Leisure", "value": 45, "color": "#82ca9d"},
            {"name": "VIP", "value": 20, "color": "#ffc658"}
        ]
    }

@app.get("/api/churn/churn-trend")
def get_churn_trend():
    """Тренд churn rate"""
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

# AI Chat endpoints
@app.post("/api/chat/message", response_model=ChatResponse)
def process_chat_message(req: ChatRequest):
    """Простой AI чат"""
    start_time = time.time()
    
    message_lower = req.message.lower()
    
    if "churn" in message_lower:
        response = """📊 **Customer Churn Analysis**

Based on our current data:
- Churn rate: 23.4% (down from 25.2% last month)
- High-risk customers: 156 identified
- Main churn factors: pricing sensitivity (35%), service issues (28%), competition (22%)

🎯 **Recommendations:**
1. Implement personalized retention campaigns for high-risk customers
2. Focus on service quality improvements in key areas
3. Consider dynamic pricing strategies for price-sensitive segments

Would you like me to dive deeper into any specific aspect of the churn analysis?"""
    
    elif "complaint" in message_lower:
        response = """🔍 **Top Complaints Analysis:**

**Most Common Issues:**
1. Room cleanliness (32% of complaints)
2. Slow room service (28% of complaints)  
3. WiFi connectivity (24% of complaints)
4. Noise disturbances (16% of complaints)

**AI Insights:**
- Complaints increased 15% this month
- Peak complaint times: 6-8 PM and 10-12 PM
- Resolution time improved by 23% with AI assistance

**Recommended Actions:**
- Implement proactive room inspection protocols
- Optimize room service delivery routes
- Upgrade WiFi infrastructure in high-traffic areas

Would you like me to generate a detailed complaint resolution report?"""
    
    elif "occupancy" in message_lower or "booking" in message_lower:
        response = """🏨 **Occupancy & Booking Analysis:**

**Current Status:**
- Occupancy rate: 78% (target: 85%)
- Booking trend: +12% vs last month
- Revenue per available room: $156

**AI Predictions:**
- Next week occupancy: 82% (high confidence)
- Peak booking periods: Tuesday-Thursday
- Optimal pricing windows identified

**Recommendations:**
- Adjust pricing for underperforming periods
- Implement targeted marketing campaigns
- Consider package deals for weekend bookings

Would you like me to show the detailed occupancy forecast?"""
    
    else:
        response = """🤖 **AI Assistant Response:**

I'm here to help you with hotel operations! I can assist you with:

📊 **Analytics & Insights:**
- Customer churn analysis and predictions
- Revenue forecasting and optimization
- Occupancy trends and booking patterns

🎯 **Operational Support:**
- Complaint analysis and resolution strategies
- Customer satisfaction insights
- Service quality recommendations

💡 **Strategic Planning:**
- Market trend analysis
- Competitive positioning
- Operational efficiency improvements

**Try asking me about:**
- "Show me the customer churn analysis"
- "What are the top complaints today?"
- "Analyze our occupancy trends"
- "Generate a satisfaction report"

How can I help you today?"""
    
    processing_time = time.time() - start_time
    
    return ChatResponse(
        response=response,
        processing_time=processing_time
    )

@app.get("/api/chat/capabilities")
def get_ai_capabilities():
    """Возможности AI"""
    return {
        "capabilities": [
            "Customer Churn Analysis",
            "Revenue Forecasting", 
            "Complaint Analysis",
            "Occupancy Predictions",
            "Satisfaction Insights",
            "Operational Recommendations"
        ],
        "supported_contexts": [
            "hotel_operations",
            "customer_service", 
            "revenue_management",
            "marketing_insights"
        ]
    }

# Call Center endpoints
@app.post("/api/call-center/process")
def process_call_message(req: ChatRequest):
    """Обработка звонков"""
    start_time = time.time()
    
    message_lower = req.message.lower()
    
    if "room service" in message_lower or "food" in message_lower:
        response = """Thank you for calling! I can help you with room service. 

🍽️ **Available Options:**
- Breakfast: 6:00 AM - 11:00 AM
- Lunch: 11:00 AM - 3:00 PM  
- Dinner: 5:00 PM - 10:00 PM
- Late Night: 10:00 PM - 2:00 AM

📋 **Popular Items:**
- Caesar Salad ($12)
- Grilled Salmon ($28)
- Margherita Pizza ($18)
- Chocolate Cake ($8)

Would you like me to connect you to our kitchen to place an order?"""
        confidence = 0.95
        escalation_needed = False
        suggested_actions = ["Connect to kitchen", "Note dietary restrictions", "Provide menu"]
    
    elif "check in" in message_lower or "check out" in message_lower:
        response = """I'd be happy to help with your check-in/out!

🏨 **Check-in Information:**
- Standard check-in: 3:00 PM
- Early check-in available (subject to availability)
- Express check-in via mobile app

🚪 **Check-out Information:**
- Standard check-out: 11:00 AM
- Late check-out available until 2:00 PM ($25 fee)
- Express check-out via mobile app

Would you like me to assist with your specific check-in/out needs?"""
        confidence = 0.92
        escalation_needed = False
        suggested_actions = ["Connect to front desk", "Schedule check-in", "Process check-out"]
    
    else:
        response = """Thank you for calling! I'm here to help with any questions about your stay.

🏨 **How I can assist you:**
- Room service and dining options
- Check-in/check-out procedures
- Hotel amenities and services
- Local area recommendations
- Billing and payment questions
- Any concerns or issues

What can I help you with today?"""
        confidence = 0.75
        escalation_needed = False
        suggested_actions = ["Connect to appropriate department", "Provide general information", "Schedule callback"]
    
    processing_time = time.time() - start_time
    
    return {
        "response": response,
        "confidence": confidence,
        "escalation_needed": escalation_needed,
        "suggested_actions": suggested_actions,
        "processing_time": processing_time
    }

@app.get("/api/call-center/stats")
def get_call_center_stats():
    """Статистика колл-центра"""
    return {
        "total_calls_today": 47,
        "ai_handled": 32,
        "avg_satisfaction": 4.3,
        "avg_duration": "2:30",
        "escalation_rate": 0.15,
        "response_time": "1.2s"
    }

# Computer Vision endpoints
@app.post("/api/computer-vision/analyze")
def analyze_image():
    """Простой анализ изображений"""
    return {
        "results": [
            {
                "type": "face",
                "confidence": 0.95,
                "description": "Hotel guest detected",
                "bounding_box": {"x": 100, "y": 50, "width": 200, "height": 250}
            },
            {
                "type": "object", 
                "confidence": 0.87,
                "description": "Luggage and bags",
                "bounding_box": {"x": 300, "y": 200, "width": 150, "height": 100}
            },
            {
                "type": "text",
                "confidence": 0.92,
                "description": "Room 1205",
                "bounding_box": {"x": 50, "y": 400, "width": 300, "height": 50}
            }
        ],
        "processing_time": 1.2,
        "image_id": "demo-001"
    }

@app.get("/api/computer-vision/capabilities")
def get_cv_capabilities():
    """Возможности Computer Vision"""
    return {
        "capabilities": [
            "Face Detection and Recognition",
            "Object Detection and Classification",
            "Text Recognition (OCR)",
            "Scene Classification",
            "Emotion Analysis",
            "Activity Recognition"
        ],
        "supported_formats": ["JPEG", "PNG", "BMP", "TIFF"],
        "max_image_size": "10MB",
        "processing_time": "1-3 seconds"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)