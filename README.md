# Monitoring System

Backend monitoring system built with a containerized architecture.

# Notice

If no threshold is configured for a metric, the metric will be stored
but no alert will be triggered.

## Tech Stack

- FastAPI (Python)
- PostgreSQL
- Redis
- Docker & Docker Compose

## Architecture

- **api**: HTTP API service
- **worker**: Background job processor
- **db**: PostgreSQL database
- **redis**: Cache / message broker

## Prerequisites

- Docker
- Docker Compose (v2+)

## Environment Variables

Environment variables are managed via `.env` file.

Create `.env` from the example:

```bash
cp .env.example .env
```

## Run the application

```bash
docker compose up --build
```

## Stop services

```bash
docker compose down
```
