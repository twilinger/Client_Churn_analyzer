from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import time

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = "hotel_operations"

class ChatResponse(BaseModel):
    response: str
    context: Optional[str] = None
    processing_time: Optional[float] = None

@router.post("/message", response_model=ChatResponse)
def process_message(req: ChatRequest):
    """Process chat message with AI assistant"""
    try:
        start_time = time.time()
        
        # Simulate AI processing
        response = generate_ai_response(req.message, req.context)
        
        processing_time = time.time() - start_time
        
        return ChatResponse(
            response=response,
            context=req.context,
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def generate_ai_response(message: str, context: str) -> str:
    """Generate AI response based on message and context"""
    message_lower = message.lower()
    
    # Hotel operations context responses
    if "churn" in message_lower or "customer" in message_lower:
        return """Based on our current analysis, I can see that:

📊 **Customer Churn Analysis:**
- Current churn rate: 23.4% (down from 25.2% last month)
- High-risk customers: 156 identified
- Main churn factors: pricing sensitivity (35%), service issues (28%), competition (22%)

🎯 **Recommendations:**
1. Implement personalized retention campaigns for high-risk customers
2. Focus on service quality improvements in key areas
3. Consider dynamic pricing strategies for price-sensitive segments

Would you like me to dive deeper into any specific aspect of the churn analysis?"""

    elif "complaint" in message_lower or "issue" in message_lower:
        return """🔍 **Top Complaints Analysis:**

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
        return """🏨 **Occupancy & Booking Analysis:**

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

    elif "satisfaction" in message_lower or "review" in message_lower:
        return """⭐ **Customer Satisfaction Insights:**

**Current Metrics:**
- Overall satisfaction: 4.2/5 (up from 3.8/5)
- NPS score: 67 (excellent)
- Response rate: 89%

**Key Satisfaction Drivers:**
1. Staff friendliness (4.6/5)
2. Room quality (4.3/5)
3. Location convenience (4.5/5)
4. Value for money (3.9/5)

**Areas for Improvement:**
- Room service speed (3.2/5)
- Amenities variety (3.7/5)

**AI Recommendations:**
- Focus on room service efficiency
- Expand amenity offerings
- Maintain current staff training programs

Would you like me to analyze specific customer feedback?"""

    elif "revenue" in message_lower or "profit" in message_lower:
        return """💰 **Revenue Analysis:**

**Financial Performance:**
- Monthly revenue: $2.4M (+8% vs last month)
- Profit margin: 34% (industry avg: 28%)
- Revenue per customer: $1,920

**Revenue Streams:**
- Room bookings: 68%
- Food & beverage: 18%
- Additional services: 14%

**AI Insights:**
- Upselling opportunities identified: $180K potential
- Optimal pricing strategies for different segments
- Revenue forecast for next quarter: +12%

**Recommendations:**
- Implement dynamic pricing for peak periods
- Enhance upselling programs
- Focus on high-value customer segments

Would you like me to generate a detailed revenue forecast?"""

    else:
        return """🤖 **AI Assistant Response:**

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

@router.get("/capabilities")
def get_ai_capabilities():
    """Get AI assistant capabilities"""
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
