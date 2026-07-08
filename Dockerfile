# Multi-stage build for Password Manager

# Stage 1: Build backend
FROM python:3.12-slim as backend-builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Build frontend
FROM node:18-alpine as frontend-builder

WORKDIR /app

# Copy frontend
COPY frontend .

# Install dependencies
RUN npm install --legacy-peer-deps

# Build frontend
RUN npm run build

# Stage 3: Final image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from backend-builder
COPY --from=backend-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend code
COPY backend /app/backend

# Copy frontend build from frontend-builder
COPY --from=frontend-builder /app/dist /app/frontend/dist

# Create data directory
RUN mkdir -p /app/data

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Start backend
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
