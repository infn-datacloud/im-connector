"""Main entry point for the IM Connector API.

This module sets up the FastAPI application, configures middleware, authentication,
and provides endpoints to interact with IM.
"""

import requests

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response as FastAPIResponse, JSONResponse as FastAPIJSONResponse
from fastapi.requests import  Request as FastAPIRquest

from im_connector.auth import configure_flaat
from im_connector.config import get_settings
from im_connector.logger import get_logger
from im_library.client.im_client import IMClient
from im_library.adapter.im_request_adapter import IMRequestAdapter

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


# IM proxy REST interface

@app.api_route("/infrastructures",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
    summary = "Proxy interface to IM",
    description = "Proxy interface to IM"
)
async def proxy_infrastructures_root(request: FastAPIRquest):
    return await forward_request(request, "infrastructures")


@app.api_route("/infrastructures/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
               summary="Proxy interface to IM (with subpath)",
               description="Proxy interface to IM (with subpath)"
)
async def proxy_infrastructures_sub(request: FastAPIRquest, path: str):
    return await forward_request(request, f"infrastructures/{path}")


async def forward_request(request: FastAPIRquest, path: str):
    url = f"{settings.IM_HOST.rstrip('/')}/{path.lstrip('/')}" if path else settings.IM_HOST.rstrip('/')

    try:
        adapter = IMRequestAdapter(request)
        backend_response = IMClient.request(adapter.request, adapter.header)

        return FastAPIResponse(
            content=backend_response.content,
            status_code=backend_response.status_code,
            headers=dict(backend_response.headers),
            media_type=backend_response.headers.get("content-type")
        )

    except requests.exceptions.RequestException as exc:
        logger = get_logger(settings)
        logger.error(f"❌ Error connecting backend: {exc}")
        return FastAPIJSONResponse(
            status_code=502,
            content={"error": f"Error connecting backend: {str(exc)}"},
        )
    except Exception as exc:
        logger = get_logger(settings)
        logger.error(f"🔥 Internal Proxy error: {exc}")
        return FastAPIJSONResponse(
            status_code=500,
            content={"error": f"IM Proxy internal error: {str(exc)}"},
        )

