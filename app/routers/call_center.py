from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import time
import uuid

router = APIRouter(prefix="/api/call-center", tags=["call-center"])

class CallProcessRequest(BaseModel):
    message: str
    context: Optional[str] = "hotel_customer_service"
    customer_id: Optional[str] = None

class CallProcessResponse(BaseModel):
    response: str
    confidence: float
    escalation_needed: bool
    suggested_actions: List[str]
    processing_time: float

class CallRecord(BaseModel):
    id: str
    customer_name: str
    phone_number: str
    duration: str
    status: str
    ai_handled: bool
    satisfaction: int
    transcript: str
    timestamp: str

@router.post("/process", response_model=CallProcessResponse)
def process_call_message(req: CallProcessRequest):
    """Process customer call message with AI"""
    try:
        start_time = time.time()
        
        # Analyze the message and generate response
        analysis = analyze_customer_message(req.message)
        
        processing_time = time.time() - start_time
        
        return CallProcessResponse(
            response=analysis["response"],
            confidence=analysis["confidence"],
            escalation_needed=analysis["escalation_needed"],
            suggested_actions=analysis["suggested_actions"],
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def analyze_customer_message(message: str) -> dict:
    """Analyze customer message and generate appropriate response"""
    message_lower = message.lower()
    
    # Room service inquiries
    if any(word in message_lower for word in ["room service", "food", "menu", "order", "delivery"]):
        return {
            "response": """Thank you for calling! I can help you with room service. 

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

Would you like me to connect you to our kitchen to place an order, or do you have any dietary restrictions I should note?""",
            "confidence": 0.95,
            "escalation_needed": False,
            "suggested_actions": ["Connect to kitchen", "Note dietary restrictions", "Provide menu"]
        }
    
    # Check-in/out inquiries
    elif any(word in message_lower for word in ["check in", "check out", "arrival", "departure", "key"]):
        return {
            "response": """I'd be happy to help with your check-in/out!

🏨 **Check-in Information:**
- Standard check-in: 3:00 PM
- Early check-in available (subject to availability)
- Express check-in via mobile app

🚪 **Check-out Information:**
- Standard check-out: 11:00 AM
- Late check-out available until 2:00 PM ($25 fee)
- Express check-out via mobile app

📱 **Mobile Services:**
- Digital key access
- Mobile check-in/out
- Real-time room status

Would you like me to assist with your specific check-in/out needs, or connect you to our front desk?""",
            "confidence": 0.92,
            "escalation_needed": False,
            "suggested_actions": ["Connect to front desk", "Schedule check-in", "Process check-out"]
        }
    
    # Complaints
    elif any(word in message_lower for word in ["problem", "issue", "complaint", "wrong", "broken", "not working"]):
        return {
            "response": """I sincerely apologize for any inconvenience you're experiencing. Let me help resolve this for you.

🔧 **Immediate Assistance:**
- I can dispatch maintenance to your room immediately
- Alternative room arrangements available
- Compensation options for service issues

📞 **Priority Support:**
- Direct line to manager: Extension 1001
- 24/7 emergency maintenance: Extension 2000
- Guest relations: Extension 3000

🎯 **Resolution Process:**
1. Immediate assessment of the issue
2. Quick resolution or alternative solution
3. Follow-up to ensure satisfaction
4. Compensation if appropriate

What specific issue are you experiencing? I'll get this resolved right away.""",
            "confidence": 0.88,
            "escalation_needed": True,
            "suggested_actions": ["Dispatch maintenance", "Offer room change", "Connect to manager", "Process compensation"]
        }
    
    # Billing inquiries
    elif any(word in message_lower for word in ["bill", "charge", "payment", "invoice", "cost", "price"]):
        return {
            "response": """I can help you with billing questions!

💳 **Billing Information:**
- Current charges visible in your account
- Itemized breakdown available
- Multiple payment methods accepted

📊 **Common Charges:**
- Room rate (varies by season)
- Room service and dining
- Spa and wellness services
- Parking ($15/night)

🔍 **Account Access:**
- Online portal: hotelname.com/account
- Mobile app billing section
- Front desk assistance

Would you like me to review your current charges or connect you to our billing department?""",
            "confidence": 0.90,
            "escalation_needed": False,
            "suggested_actions": ["Review charges", "Connect to billing", "Process payment", "Explain charges"]
        }
    
    # General information
    else:
        return {
            "response": """Thank you for calling! I'm here to help with any questions about your stay.

🏨 **How I can assist you:**
- Room service and dining options
- Check-in/check-out procedures
- Hotel amenities and services
- Local area recommendations
- Billing and payment questions
- Any concerns or issues

📞 **Direct Connections:**
- Front Desk: Extension 1000
- Concierge: Extension 2000
- Manager: Extension 1001

What can I help you with today?""",
            "confidence": 0.75,
            "escalation_needed": False,
            "suggested_actions": ["Connect to appropriate department", "Provide general information", "Schedule callback"]
        }

@router.get("/stats")
def get_call_center_stats():
    """Get call center statistics"""
    return {
        "total_calls_today": 47,
        "ai_handled": 32,
        "avg_satisfaction": 4.3,
        "avg_duration": "2:30",
        "escalation_rate": 0.15,
        "response_time": "1.2s"
    }

@router.get("/recent-calls")
def get_recent_calls():
    """Get recent call records"""
    return {
        "calls": [
            {
                "id": "1",
                "customer_name": "John Smith",
                "phone_number": "+1-555-0123",
                "duration": "3:45",
                "status": "completed",
                "ai_handled": True,
                "satisfaction": 5,
                "transcript": "Customer called about room service. AI provided automated response with menu options.",
                "timestamp": "2024-01-15 14:30"
            },
            {
                "id": "2", 
                "customer_name": "Maria Garcia",
                "phone_number": "+1-555-0124",
                "duration": "2:15",
                "status": "completed",
                "ai_handled": False,
                "satisfaction": 4,
                "transcript": "Customer needed help with check-in. Escalated to human agent.",
                "timestamp": "2024-01-15 13:45"
            }
        ]
    }

@router.post("/start-call")
def start_call():
    """Start a new call session"""
    call_id = str(uuid.uuid4())
    return {
        "call_id": call_id,
        "status": "active",
        "timestamp": time.time()
    }

@router.post("/end-call/{call_id}")
def end_call(call_id: str):
    """End a call session"""
    return {
        "call_id": call_id,
        "status": "completed",
        "duration": "2:30",
        "timestamp": time.time()
    }
