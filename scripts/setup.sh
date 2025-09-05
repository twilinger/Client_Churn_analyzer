#!/bin/bash

# Hotel AI Suite Setup Script
# This script sets up the development environment

set -e

echo "🏨 Setting up Hotel AI Suite..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    echo "✅ Prerequisites check passed"
}

# Setup environment
setup_environment() {
    echo "🔧 Setting up environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo "📝 Creating .env file..."
        cat > .env << EOF
# Application Configuration
APP_TITLE=Hotel AI Suite
APP_VERSION=1.0.0
DEBUG=true

# Database Configuration
DATABASE_URL=postgresql://hotel_user:hotel_password@postgres:5432/hotel_ai
REDIS_URL=redis://redis:6379

# AI Services
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=llama3
VECTOR_DB_PATH=/app/data/rag_db

# Security
SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# External Services (Optional)
OPENAI_API_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
EOF
        echo "✅ .env file created"
    else
        echo "✅ .env file already exists"
    fi
}

# Setup directories
setup_directories() {
    echo "📁 Setting up directories..."
    
    mkdir -p data/rag_db
    mkdir -p logs
    mkdir -p uploads
    
    echo "✅ Directories created"
}

# Pull and start services
start_services() {
    echo "🚀 Starting services..."
    
    # Pull images
    docker-compose pull
    
    # Start services
    docker-compose up -d
    
    echo "✅ Services started"
}

# Wait for services to be ready
wait_for_services() {
    echo "⏳ Waiting for services to be ready..."
    
    # Wait for database
    echo "Waiting for PostgreSQL..."
    until docker-compose exec -T postgres pg_isready -U hotel_user; do
        sleep 2
    done
    
    # Wait for Redis
    echo "Waiting for Redis..."
    until docker-compose exec -T redis redis-cli ping; do
        sleep 2
    done
    
    # Wait for Ollama
    echo "Waiting for Ollama..."
    until curl -f http://localhost:11434/api/tags &> /dev/null; do
        sleep 5
    done
    
    echo "✅ All services are ready"
}

# Setup AI models
setup_ai_models() {
    echo "🤖 Setting up AI models..."
    
    # Pull Llama3 model
    docker-compose exec ollama ollama pull llama3
    
    echo "✅ AI models ready"
}

# Run initial setup
run_initial_setup() {
    echo "🔨 Running initial setup..."
    
    # Run database migrations
    docker-compose exec hotel-ai-app python -c "
from Backend.app.utils.settings import settings
from sqlalchemy import create_engine
import pandas as pd

# Create database tables
engine = create_engine(settings.DATABASE_URL)
print('Database connection established')

# Load sample data
df = pd.read_csv('data/raw/Telco-Customer-Churn.csv')
df.to_sql('customers', engine, if_exists='replace', index=False)
print('Sample data loaded')
"
    
    echo "✅ Initial setup completed"
}

# Display access information
show_access_info() {
    echo ""
    echo "🎉 Hotel AI Suite is ready!"
    echo ""
    echo "📱 Access Points:"
    echo "   Application: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo "   ReDoc: http://localhost:8000/redoc"
    echo "   Ollama: http://localhost:11434"
    echo ""
    echo "🔧 Management Commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Stop services: docker-compose down"
    echo "   Restart: docker-compose restart"
    echo "   Update: docker-compose pull && docker-compose up -d"
    echo ""
    echo "📚 Documentation:"
    echo "   README.md - Project overview"
    echo "   docs/API.md - API documentation"
    echo "   docs/DEPLOYMENT.md - Deployment guide"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_environment
    setup_directories
    start_services
    wait_for_services
    setup_ai_models
    run_initial_setup
    show_access_info
}

# Run main function
main "$@"
