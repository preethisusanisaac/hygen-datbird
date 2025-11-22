#!/bin/bash
# Start script for production deployment

# Run database initialization if needed
# python -c "from app.models.db import init_db; init_db()"

# Start uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
