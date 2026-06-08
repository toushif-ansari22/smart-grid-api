# Smart Grid Load Balancing API

Built for Infotact Solutions Technical Internship Program 2026

## Project Overview
A high-performance Python backend for a Smart Grid Operations Center.
Real-time telemetry ingestion, load balancing, and WebSocket alerts.

## Tech Stack
- FastAPI + Python 3.11
- TimescaleDB (PostgreSQL)
- Celery + Redis
- Docker Compose
- WebSocket

## API Endpoints
- POST /api/v1/meter/reading — Ingest smart meter data
- GET /api/v1/meter/readings/{city_zone} — Get zone readings
- GET /api/v1/grid/status/{city_zone} — Get grid status
- WS /ws/alerts — Real-time WebSocket alerts

## Run Locally
docker-compose up --build

## API Docs
http://localhost:8000/docs

## Author
Toushif Ansari — Python Development Intern
University Polytechnic, BIT Mesra