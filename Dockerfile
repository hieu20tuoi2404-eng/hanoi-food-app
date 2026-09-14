# Multi-stage production image: build frontend with Node, serve everything via FastAPI.

# ---------- Stage 1: build frontend ----------
FROM node:20-alpine AS frontend

WORKDIR /build/frontend

COPY frontend/package.json ./
RUN npm install --no-audit --no-fund

COPY frontend/ ./
RUN npm run build

# ---------- Stage 2: backend (serves API + static frontend) ----------
FROM python:3.12-slim AS backend

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
COPY --from=frontend /build/frontend/dist /frontend/dist

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}