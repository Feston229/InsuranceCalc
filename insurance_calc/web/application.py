import logging

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from insurance_calc.settings import settings
from insurance_calc.web.api.router import api_router
from importlib import metadata

from insurance_calc.web.lifespan import lifespan_setup
from insurance_calc.log import configure_logging


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="insurance_calc",
        version=metadata.version("insurance_calc"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
