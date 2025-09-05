from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils.settings import settings
from .routers import churn, chat, call_center, computer_vision

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE, 
        version=settings.APP_VERSION,
        description="AI-powered hotel customer service and analytics platform",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(churn.router)
    app.include_router(chat.router)
    app.include_router(call_center.router)
    app.include_router(computer_vision.router)
    
    return app

app = create_app()
