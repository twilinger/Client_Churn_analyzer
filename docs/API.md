# API Documentation

## Overview

The Hotel AI Suite provides a comprehensive REST API for hotel operations, customer analytics, and AI-powered services.

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints require authentication via JWT tokens (implementation ready).

## Endpoints

### Churn Analysis

#### Predict Customer Churn
```http
POST /api/churn/predict
Content-Type: application/json

{
  "features_vector": [0.1, 0.2, 0.3, ...],
  "features_dict": {
    "contract": "Month-to-month",
    "payment_method": "Electronic check",
    "monthly_charges": 70.35
  },
  "extra_context": "Customer has been complaining about service"
}
```

**Response:**
```json
{
  "churn_proba": 0.85
}
```

#### Explain Churn Prediction
```http
POST /api/churn/explain
Content-Type: application/json

{
  "features_vector": [0.1, 0.2, 0.3, ...],
  "features_dict": {...},
  "extra_context": "..."
}
```

**Response:**
```json
{
  "base_value": 0.5,
  "contributions": [
    {
      "feature": "contract",
      "value": "Month-to-month",
      "contribution": 0.3
    }
  ],
  "top_k": 8,
  "reason": "High churn risk due to month-to-month contract"
}
```

#### Dashboard Statistics
```http
GET /api/churn/dashboard-stats
```

**Response:**
```json
{
  "total_customers": 1247,
  "churn_rate": 23.4,
  "ai_interactions": 3421,
  "satisfaction_score": 4.2,
  "high_risk_customers": 156,
  "avg_response_time": "1.2s"
}
```

### AI Chat

#### Send Message
```http
POST /api/chat/message
Content-Type: application/json

{
  "message": "Show me the customer churn analysis",
  "context": "hotel_operations"
}
```

**Response:**
```json
{
  "response": "Based on our current analysis...",
  "context": "hotel_operations",
  "processing_time": 1.2
}
```

#### Get AI Capabilities
```http
GET /api/chat/capabilities
```

**Response:**
```json
{
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
```

### Call Center

#### Process Call Message
```http
POST /api/call-center/process
Content-Type: application/json

{
  "message": "I need room service",
  "context": "hotel_customer_service",
  "customer_id": "12345"
}
```

**Response:**
```json
{
  "response": "Thank you for calling! I can help you with room service...",
  "confidence": 0.95,
  "escalation_needed": false,
  "suggested_actions": [
    "Connect to kitchen",
    "Note dietary restrictions",
    "Provide menu"
  ],
  "processing_time": 0.8
}
```

#### Get Call Center Stats
```http
GET /api/call-center/stats
```

**Response:**
```json
{
  "total_calls_today": 47,
  "ai_handled": 32,
  "avg_satisfaction": 4.3,
  "avg_duration": "2:30",
  "escalation_rate": 0.15,
  "response_time": "1.2s"
}
```

### Computer Vision

#### Analyze Image
```http
POST /api/computer-vision/analyze
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "results": [
    {
      "type": "face",
      "confidence": 0.95,
      "description": "Human face detected",
      "bounding_box": {
        "x": 100,
        "y": 50,
        "width": 200,
        "height": 250
      }
    }
  ],
  "processing_time": 1.2,
  "image_id": "uuid-string"
}
```

#### Get CV Capabilities
```http
GET /api/computer-vision/capabilities
```

**Response:**
```json
{
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
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

- **Default**: 100 requests per minute per IP
- **AI Endpoints**: 20 requests per minute per user
- **File Upload**: 10 requests per minute per user

## WebSocket Support

Real-time updates available for:
- Live call center metrics
- Real-time AI processing status
- Dashboard updates

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/dashboard');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Update dashboard
};
```
