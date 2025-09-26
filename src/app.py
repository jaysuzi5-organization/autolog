import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import health, info, vehicle, gas
from dependencies import setup_db

# Setup logging before anything else uses it
logger = logging.getLogger(__name__)

from framework.middleware import LoggingMiddleware

app = FastAPI(
    title="Autolog API",
    version="1.0.0",
    openapi_url="/api/v1/autolog/openapi.json",
    docs_url="/api/v1/autolog/docs"
)

for mw in [LoggingMiddleware]:
    app.add_middleware(mw)

setup_db(logger)

# Register routes
app.include_router(health.router, tags=["Health"])
app.include_router(info.router, tags=["Info"])
app.include_router(vehicle.router, tags=["vehicle"])
app.include_router(gas.router, tags=["gas"])
app.mount("/autolog/test", StaticFiles(directory="static", html=True), name="test")
