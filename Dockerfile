# Multi-stage build for Hotel AI Suite
FROM node:18-alpine AS frontend-build

# Set working directory for frontend
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY frontend/ ./

# Build frontend
RUN npm run build

# Python backend stage
FROM python:3.11-slim AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_NO_TF=1
ENV TF_ENABLE_ONEDNN_OPTS=0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY Backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY Backend/ ./Backend/
COPY core/ ./core/
COPY db/ ./db/
COPY data/ ./data/
COPY rag/ ./rag/
COPY knowledge/ ./knowledge/

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run the application
CMD ["uvicorn", "Backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
