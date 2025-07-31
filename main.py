"""Main entry point for the IM Connector API.

This module sets up the FastAPI application, configures middleware, authentication,
and provides endpoints to interact with IM.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response as FastAPIResponse

from im_connector.im import create_k8s_deployment
from im_connector.models import DeploymentCreate
from auth import check_authorization, configure_flaat, HttpAuthzCredsDep
from config import get_settings, SettingsDep
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
async def create_kubernetes_deployment(payload: DeploymentCreate, credentials: HttpAuthzCredsDep,
                                       app_settings: SettingsDep) -> FastAPIResponse:
    response: FastAPIResponse = create_k8s_deployment(
        im_url=payload.im_url,
        im_access_token=payload.im_access_token,
        iaas_access_token=payload.iaas_access_token,
        tosca_template=payload.tosca_template,
        provider_name=payload.provider_name,
        provider_endpoint=payload.provider_endpoint,
        provider_type=payload.provider_type)

    return response
