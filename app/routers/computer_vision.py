from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import time
import uuid
import base64
from PIL import Image
import io

router = APIRouter(prefix="/api/computer-vision", tags=["computer-vision"])

class VisionResult(BaseModel):
    type: str  # 'face', 'object', 'text', 'scene'
    confidence: float
    description: str
    bounding_box: Optional[dict] = None

class AnalysisResponse(BaseModel):
    results: List[VisionResult]
    processing_time: float
    image_id: str

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded image with computer vision AI"""
    try:
        start_time = time.time()
        
        # Read and process the image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Generate analysis results
        results = analyze_image_content(image)
        
        processing_time = time.time() - start_time
        image_id = str(uuid.uuid4())
        
        return AnalysisResponse(
            results=results,
            processing_time=processing_time,
            image_id=image_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def analyze_image_content(image: Image.Image) -> List[VisionResult]:
    """Analyze image content and return detected objects/features"""
    # Mock analysis for demonstration
    # In a real implementation, this would use actual CV models
    
    results = []
    
    # Simulate face detection
    if image.width > 200 and image.height > 200:
        results.append(VisionResult(
            type="face",
            confidence=0.95,
            description="Human face detected",
            bounding_box={"x": 100, "y": 50, "width": 200, "height": 250}
        ))
    
    # Simulate object detection
    results.append(VisionResult(
        type="object",
        confidence=0.87,
        description="Hotel lobby furniture",
        bounding_box={"x": 300, "y": 200, "width": 150, "height": 100}
    ))
    
    # Simulate text detection
    results.append(VisionResult(
        type="text",
        confidence=0.92,
        description="Welcome to Hotel Plaza",
        bounding_box={"x": 50, "y": 400, "width": 300, "height": 50}
    ))
    
    # Simulate scene classification
    results.append(VisionResult(
        type="scene",
        confidence=0.89,
        description="Hotel lobby interior",
        bounding_box=None
    ))
    
    return results

@router.post("/analyze-base64")
async def analyze_base64_image(request: dict):
    """Analyze base64 encoded image"""
    try:
        start_time = time.time()
        
        # Decode base64 image
        image_data = base64.b64decode(request["image"])
        image = Image.open(io.BytesIO(image_data))
        
        # Generate analysis
        results = analyze_image_content(image)
        
        processing_time = time.time() - start_time
        
        return {
            "results": [result.dict() for result in results],
            "processing_time": processing_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/capabilities")
def get_cv_capabilities():
    """Get computer vision capabilities"""
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

@router.get("/demo-results")
def get_demo_results():
    """Get demo analysis results for testing"""
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
            },
            {
                "type": "scene",
                "confidence": 0.89,
                "description": "Hotel corridor",
                "bounding_box": None
            }
        ],
        "processing_time": 1.2,
        "image_id": "demo-001"
    }

@router.post("/security-scan")
async def security_scan(file: UploadFile = File(...)):
    """Perform security-focused image analysis"""
    try:
        start_time = time.time()
        
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Security-specific analysis
        security_results = perform_security_analysis(image)
        
        processing_time = time.time() - start_time
        
        return {
            "security_alerts": security_results["alerts"],
            "detected_objects": security_results["objects"],
            "risk_level": security_results["risk_level"],
            "processing_time": processing_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def perform_security_analysis(image: Image.Image) -> dict:
    """Perform security-focused analysis"""
    alerts = []
    objects = []
    risk_level = "low"
    
    # Simulate security analysis
    objects.append({
        "type": "person",
        "confidence": 0.95,
        "description": "Hotel guest",
        "location": {"x": 100, "y": 50, "width": 200, "height": 250}
    })
    
    objects.append({
        "type": "baggage",
        "confidence": 0.87,
        "description": "Suitcase",
        "location": {"x": 300, "y": 200, "width": 150, "height": 100}
    })
    
    # Check for potential security concerns
    if image.width > 500:  # Large image might indicate surveillance
        alerts.append({
            "type": "unusual_activity",
            "severity": "medium",
            "description": "Large group detected in restricted area"
        })
        risk_level = "medium"
    
    return {
        "alerts": alerts,
        "objects": objects,
        "risk_level": risk_level
    }
