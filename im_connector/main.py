"""Main entry point for the IM Connector API.

This module sets up the FastAPI application, configures middleware, authentication,
and provides endpoints to interact with IM.
"""

import requests

from contextlib import asynccontextmanager

from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response as FastAPIResponse, JSONResponse as FastAPIJSONResponse
from fastapi.requests import  Request as FastAPIRquest

from im_connector.im import create_k8s_deployment
from im_connector.models import DeploymentCreate
from im_connector.auth import check_authorization, configure_flaat, HttpAuthzCredsDep
from im_connector.config import get_settings, SettingsDep
from im_connector.logger import get_logger

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


# IM proxy REST interface

# 🔹 Registry demo local handlers
def local_status_handler(request: FastAPIRquest):
    return FastAPIJSONResponse({"service": "proxy", "status": "ok"}, status_code=200)

def healthcheck_handler(request: FastAPIRquest):
    return FastAPIJSONResponse({"health": "green", "uptime": "12345s"}, status_code=200)

# local paths map for demo, put here actual paths
LOCAL_ROUTES = {
    "infrastructures/proxylocalstatus": local_status_handler,
    "infrastructures/proxyhealthcheck": healthcheck_handler,
}


@app.api_route("/infrastructures/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    summary = "Proxy interface to IM",
    description = "Proxy interface to IM",
    dependencies = [Security(check_authorization)]
)
def proxy(request: FastAPIRquest, path: str):

    url = f"{SettingsDep.IM_HOST}/infrastructures/{path}"

    try:

        if path in LOCAL_ROUTES:
            return LOCAL_ROUTES[path](request)
        
        body = request.body()
        excluded_headers = {"host", "content-length", "connection"}
        headers = {k: v for k, v in request.headers.items() if k.lower() not in excluded_headers}

        backend_response = requests.request(
            method=request.method,
            url=url,
            params=request.query_params,
            data=body,
            headers=headers,
            timeout=30.0,
        )

        return FastAPIResponse(
            content=backend_response.content,
            status_code=backend_response.status_code,
            headers=dict(backend_response.headers),
            media_type=backend_response.headers.get("content-type")
        )

    except requests.exceptions.RequestException as exc:
        print(f"❌ Error connecting backend: {exc}")
        return FastAPIJSONResponse(
            status_code=502,
            content={"error": f"Error connecting backend: {str(exc)}"},
        )
    except Exception as exc:
        print(f"🔥 Internal Proxy error: {exc}")
        return FastAPIJSONResponse(
            status_code=500,
            content={"error": f"IM Proxy internal error: {str(exc)}"},
        )

