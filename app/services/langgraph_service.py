"""
LangGraph-based AI service for hotel operations
Demonstrates advanced NLP capabilities with workflow orchestration
"""

from typing import Dict, List, Any, Optional
from langgraph.graph import StateGraph, END
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import json
import time

class HotelAIAgent:
    """Advanced AI agent using LangGraph for hotel operations"""
    
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.llm = Ollama(model=model_name)
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.vectorstore = None
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow for hotel AI operations"""
        
        # Define the state structure
        class HotelAIState:
            def __init__(self):
                self.messages: List[BaseMessage] = []
                self.context: Dict[str, Any] = {}
                self.intent: str = ""
                self.response: str = ""
                self.confidence: float = 0.0
                self.next_action: str = ""
        
        # Define workflow nodes
        def intent_classifier(state: HotelAIState) -> HotelAIState:
            """Classify user intent"""
            last_message = state.messages[-1].content.lower()
            
            if any(word in last_message for word in ["churn", "customer", "leave", "cancel"]):
                state.intent = "churn_analysis"
                state.confidence = 0.9
            elif any(word in last_message for word in ["complaint", "problem", "issue", "wrong"]):
                state.intent = "complaint_handling"
                state.confidence = 0.85
            elif any(word in last_message for word in ["booking", "reservation", "room", "check"]):
                state.intent = "booking_assistance"
                state.confidence = 0.8
            elif any(word in last_message for word in ["revenue", "money", "price", "cost"]):
                state.intent = "revenue_analysis"
                state.confidence = 0.8
            else:
                state.intent = "general_inquiry"
                state.confidence = 0.6
                
            return state
        
        def context_retriever(state: HotelAIState) -> HotelAIState:
            """Retrieve relevant context from knowledge base"""
            # Mock context retrieval
            context_map = {
                "churn_analysis": {
                    "current_churn_rate": 23.4,
                    "high_risk_customers": 156,
                    "main_factors": ["pricing", "service", "competition"],
                    "recommendations": ["retention_campaigns", "service_improvement", "pricing_strategy"]
                },
                "complaint_handling": {
                    "top_complaints": ["cleanliness", "room_service", "wifi", "noise"],
                    "resolution_time": "2.3 hours",
                    "satisfaction_rate": 87.5,
                    "escalation_rate": 15.2
                },
                "booking_assistance": {
                    "occupancy_rate": 78.5,
                    "booking_trend": "+12%",
                    "peak_periods": ["Tuesday-Thursday"],
                    "available_rooms": 45
                },
                "revenue_analysis": {
                    "monthly_revenue": 2400000,
                    "profit_margin": 34.2,
                    "revenue_streams": {"rooms": 68, "f&b": 18, "services": 14},
                    "forecast": "+12%"
                }
            }
            
            state.context = context_map.get(state.intent, {})
            return state
        
        def response_generator(state: HotelAIState) -> HotelAIState:
            """Generate AI response based on intent and context"""
            intent = state.intent
            context = state.context
            last_message = state.messages[-1].content
            
            if intent == "churn_analysis":
                state.response = f"""📊 **Customer Churn Analysis**

Based on our current data:
- Churn rate: {context.get('current_churn_rate', 23.4)}%
- High-risk customers: {context.get('high_risk_customers', 156)}
- Main factors: {', '.join(context.get('main_factors', ['pricing', 'service']))}

🎯 **AI Recommendations:**
1. Implement personalized retention campaigns
2. Focus on service quality improvements  
3. Consider dynamic pricing strategies

Would you like me to analyze specific customer segments or generate retention strategies?"""
                
            elif intent == "complaint_handling":
                state.response = f"""🔍 **Complaint Analysis & Resolution**

**Current Status:**
- Top complaints: {', '.join(context.get('top_complaints', ['cleanliness', 'service']))}
- Avg resolution time: {context.get('resolution_time', '2.3 hours')}
- Satisfaction rate: {context.get('satisfaction_rate', 87.5)}%

**AI-Powered Solutions:**
- Automated complaint categorization
- Priority-based routing
- Proactive issue detection
- Customer satisfaction tracking

I can help you analyze specific complaints or implement resolution strategies."""
                
            elif intent == "booking_assistance":
                state.response = f"""🏨 **Booking & Occupancy Insights**

**Current Status:**
- Occupancy rate: {context.get('occupancy_rate', 78.5)}%
- Booking trend: {context.get('booking_trend', '+12%')}
- Available rooms: {context.get('available_rooms', 45)}

**AI Recommendations:**
- Dynamic pricing optimization
- Targeted marketing campaigns
- Peak period management
- Revenue maximization strategies

Would you like assistance with specific booking scenarios or occupancy optimization?"""
                
            elif intent == "revenue_analysis":
                state.response = f"""💰 **Revenue Analysis & Forecasting**

**Financial Performance:**
- Monthly revenue: ${context.get('monthly_revenue', 2400000):,}
- Profit margin: {context.get('profit_margin', 34.2)}%
- Revenue streams: {context.get('revenue_streams', {})}

**AI Insights:**
- Revenue forecast: {context.get('forecast', '+12%')}
- Upselling opportunities identified
- Optimal pricing strategies
- Market trend analysis

I can provide detailed revenue breakdowns or forecasting models."""
                
            else:
                state.response = """🤖 **AI Assistant Response**

I'm here to help with hotel operations! I can assist you with:

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

What specific area would you like to explore?"""
            
            state.next_action = "provide_response"
            return state
        
        def response_enhancer(state: HotelAIState) -> HotelAIState:
            """Enhance response with additional context"""
            if state.confidence > 0.8:
                state.response += "\n\n✨ *High confidence analysis - recommendations based on latest data*"
            elif state.confidence > 0.6:
                state.response += "\n\n⚠️ *Moderate confidence - consider additional data sources*"
            else:
                state.response += "\n\n❓ *Low confidence - recommend human review*"
            
            return state
        
        # Build the graph
        workflow = StateGraph(HotelAIState)
        
        # Add nodes
        workflow.add_node("intent_classifier", intent_classifier)
        workflow.add_node("context_retriever", context_retriever)
        workflow.add_node("response_generator", response_generator)
        workflow.add_node("response_enhancer", response_enhancer)
        
        # Define edges
        workflow.set_entry_point("intent_classifier")
        workflow.add_edge("intent_classifier", "context_retriever")
        workflow.add_edge("context_retriever", "response_generator")
        workflow.add_edge("response_generator", "response_enhancer")
        workflow.add_edge("response_enhancer", END)
        
        return workflow.compile()
    
    def process_message(self, message: str, context: str = "hotel_operations") -> Dict[str, Any]:
        """Process user message through LangGraph workflow"""
        try:
            # Create initial state
            state = type('HotelAIState', (), {
                'messages': [HumanMessage(content=message)],
                'context': {},
                'intent': "",
                'response': "",
                'confidence': 0.0,
                'next_action': ""
            })()
            
            # Execute workflow
            result = self.graph.invoke(state)
            
            return {
                "response": result.response,
                "intent": result.intent,
                "confidence": result.confidence,
                "context": result.context,
                "processing_time": time.time()
            }
            
        except Exception as e:
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "intent": "error",
                "confidence": 0.0,
                "context": {},
                "processing_time": time.time()
            }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get AI agent capabilities"""
        return {
            "intents_supported": [
                "churn_analysis",
                "complaint_handling", 
                "booking_assistance",
                "revenue_analysis",
                "general_inquiry"
            ],
            "workflow_steps": [
                "intent_classification",
                "context_retrieval",
                "response_generation",
                "response_enhancement"
            ],
            "confidence_thresholds": {
                "high": 0.8,
                "medium": 0.6,
                "low": 0.4
            }
        }

# Global instance
hotel_ai_agent = HotelAIAgent()
