"""
app.py

Entry point for the FastAPI application.  
Configures logging, middleware, database connections, routes, and OpenTelemetry instrumentation.

This application follows a modular architecture:
- API endpoints are defined in `api/` modules.
- Database models are located in `models/`.
- Middleware and instrumentation logic is in `framework/`.

Environment Variables:
    TESTING (str): If set to `"true"`, disables middleware and OpenTelemetry, and uses basic logging.

"""

import os
import logging
from time import sleep
from fastapi import FastAPI
from sqlalchemy import text
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from framework.db import Database
from models.base import Base
from api import health, info, vehicle

# Setup logging before anything else uses it
logger = logging.getLogger(__name__)

from framework.middleware import LoggingMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
app_middleware = [LoggingMiddleware]
otel_enabled = True
max_retries = 5
retry_delay = 2
database = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events for the FastAPI application.
    On startup:
        - Attempts to establish a database connection.
        - Retries connection up to `max_retries` times with `retry_delay` seconds between attempts.
        - Initializes database tables if they do not exist.

    Args:
        app (FastAPI): The FastAPI application instance.

    Raises:
        Exception: If database connection fails after the maximum number of retries.

    Yields:
        None: Control is returned to the application after startup logic completes.
    """

    global database
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting database connection (attempt {attempt + 1}/{max_retries})")
            database = Database(Base)
            session = database.get_session()
            session.execute(text("SELECT 1"))
            session.close()
            logger.info("Database connection established successfully")
            break
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            if attempt == max_retries - 1:
                logger.error("Max retries reached, failing startup")
                raise
            sleep(retry_delay)

def get_db():
    if database:
        db = database.get_session()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None

app = FastAPI(
    title="Autolog API",
    version="1.0.0",
    openapi_url="/api/v1/autolog/openapi.json",
    docs_url="/api/v1/autolog/docs",
    lifespan=lifespan
)

# Add middleware and instrumentation
if os.getenv("TESTING") != "true":
    for mw in app_middleware:
        app.add_middleware(mw)
    if otel_enabled:
        FastAPIInstrumentor.instrument_app(app)

# Register routes
app.include_router(health.router, tags=["Health"])
app.include_router(info.router, tags=["Info"])
app.include_router(vehicle.router, tags=["vehicle"])
app.mount("/autolog/test", StaticFiles(directory="static", html=True), name="test")
