"""Main entry point for the IM Connector API.

This module sets up the FastAPI application, configures middleware, authentication,
and provides endpoints to interact with IM.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Security
from fastapi.middleware.cors import CORSMiddleware

from api.im import create_k8s_deployment
from auth import check_authorization, configure_flaat
from config import get_settings
from logger import get_logger

settings = get_settings()

title = "IM Connector API"
summary = "IM Connector REST API"
description = "This API provides endpoints to interact with IM"
version = "0.1.0"
docs_url = "/docs"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI application lifespan context manager.

    This function is called at application startup and shutdown. It performs:
    - Initializes the application logger and attaches it to the request state.
    - Configures authentication/authorization (Flaat).

    Args:
        app: The FastAPI application instance.

    Yields:
        dict: A dictionary with the logger instance, available in the request state.

    """
    logger = get_logger(settings)
    configure_flaat(settings, logger)
    yield {"logger": logger}


# Create FastAPI app
app = FastAPI(
    title=title,
    summary=summary,
    description=description,
    version=version,
    docs_url=docs_url,
    lifespan=lifespan,
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).rstrip("/") for origin in settings.ALLOWED_ORIGINS
    ],  # or ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/api/v1/deployments",
    summary="Create Kubernetes Deployment",
    description="Given a TOSCA template, trigger the InfrastructureManager to create a Kubernetes deployment",
    dependencies=[Security(check_authorization)]
)
async def create_kubernetes_deployment(request: Request):
    # request.headers <-- recuperiamo token?
    # request.body    <-- recuperiamo tosca?
    im_url = settings.IM_HOST
    jwt = request.headers
    tosca_template = request.body

    status = create_k8s_deployment(im_url, jwt, tosca_template)

    return status
