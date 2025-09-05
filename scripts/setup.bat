@echo off
REM Hotel AI Suite Setup Script for Windows
REM This script sets up the development environment

echo 🏨 Setting up Hotel AI Suite...

REM Check prerequisites
echo 📋 Checking prerequisites...

where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Setup environment
echo 🔧 Setting up environment...

if not exist .env (
    echo 📝 Creating .env file...
    (
        echo # Application Configuration
        echo APP_TITLE=Hotel AI Suite
        echo APP_VERSION=1.0.0
        echo DEBUG=true
        echo.
        echo # Database Configuration
        echo DATABASE_URL=postgresql://hotel_user:hotel_password@postgres:5432/hotel_ai
        echo REDIS_URL=redis://redis:6379
        echo.
        echo # AI Services
        echo OLLAMA_HOST=http://ollama:11434
        echo OLLAMA_MODEL=llama3
        echo VECTOR_DB_PATH=/app/data/rag_db
        echo.
        echo # Security
        echo SECRET_KEY=dev-secret-key-change-in-production
        echo JWT_ALGORITHM=HS256
        echo JWT_EXPIRE_MINUTES=1440
        echo.
        echo # External Services ^(Optional^)
        echo OPENAI_API_KEY=
        echo AWS_ACCESS_KEY_ID=
        echo AWS_SECRET_ACCESS_KEY=
    ) > .env
    echo ✅ .env file created
) else (
    echo ✅ .env file already exists
)

REM Setup directories
echo 📁 Setting up directories...

if not exist data\rag_db mkdir data\rag_db
if not exist logs mkdir logs
if not exist uploads mkdir uploads

echo ✅ Directories created

REM Start services
echo 🚀 Starting services...

docker-compose pull
docker-compose up -d

echo ✅ Services started

REM Wait for services
echo ⏳ Waiting for services to be ready...

:wait_postgres
docker-compose exec -T postgres pg_isready -U hotel_user >nul 2>nul
if %errorlevel% neq 0 (
    timeout /t 2 >nul
    goto wait_postgres
)
echo ✅ PostgreSQL is ready

:wait_redis
docker-compose exec -T redis redis-cli ping >nul 2>nul
if %errorlevel% neq 0 (
    timeout /t 2 >nul
    goto wait_redis
)
echo ✅ Redis is ready

:wait_ollama
curl -f http://localhost:11434/api/tags >nul 2>nul
if %errorlevel% neq 0 (
    timeout /t 5 >nul
    goto wait_ollama
)
echo ✅ Ollama is ready

REM Setup AI models
echo 🤖 Setting up AI models...
docker-compose exec ollama ollama pull llama3
echo ✅ AI models ready

REM Run initial setup
echo 🔨 Running initial setup...
docker-compose exec hotel-ai-app python -c "from Backend.app.utils.settings import settings; from sqlalchemy import create_engine; import pandas as pd; engine = create_engine(settings.DATABASE_URL); print('Database connection established'); df = pd.read_csv('data/raw/Telco-Customer-Churn.csv'); df.to_sql('customers', engine, if_exists='replace', index=False); print('Sample data loaded')"
echo ✅ Initial setup completed

REM Display access information
echo.
echo 🎉 Hotel AI Suite is ready!
echo.
echo 📱 Access Points:
echo    Application: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo    ReDoc: http://localhost:8000/redoc
echo    Ollama: http://localhost:11434
echo.
echo 🔧 Management Commands:
echo    View logs: docker-compose logs -f
echo    Stop services: docker-compose down
echo    Restart: docker-compose restart
echo    Update: docker-compose pull ^&^& docker-compose up -d
echo.
echo 📚 Documentation:
echo    README.md - Project overview
echo    docs/API.md - API documentation
echo    docs/DEPLOYMENT.md - Deployment guide
echo.

pause
