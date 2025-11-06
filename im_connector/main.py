"""Main entry point for the IM Connector API.

This module sets up the FastAPI application, configures middleware, authentication,
and provides endpoints to interact with IM.
"""

from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request as FastAPIRequest
from fastapi.responses import JSONResponse as FastAPIJSONResponse

from im_connector.auth import configure_flaat
from im_connector.config import get_settings
from im_connector.fastapi_response_wrapper import FastAPIResponseWrapper
from im_connector.logger import get_logger
from im_library.adapter.im_request_adapter import IMRequestAdapter
from im_library.client.im_client import IMClient

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
async def proxy_infrastructures_root(request: FastAPIRequest):
    return await forward_request(request)


@app.api_route("/infrastructures/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
               summary="Proxy interface to IM (with subpath)",
               description="Proxy interface to IM (with subpath)"
)
async def proxy_infrastructures_sub(request: FastAPIRequest):
    return await forward_request(request)


async def forward_request(request: FastAPIRequest):
    try:
        request_body = await request.body()
        adapter = IMRequestAdapter(request, request_body)
        try:
         backend_response = IMClient.request(adapter.request, adapter.header)
        except Exception as e:
            # Relaying the exception to ensure consistency with FastAPI data types
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=e)

        if not backend_response.ok:
            raise HTTPException(status_code=backend_response.status_code, detail=backend_response.reason)

        return FastAPIResponseWrapper(backend_response)
    except requests.exceptions.RequestException as exc:
        logger = get_logger(settings)
        logger.error(f"Error connecting backend: {exc}")
        return FastAPIJSONResponse(
            status_code=502,
            content={"error": f"Error connecting backend: {str(exc)}"},
        )
    except Exception as exc:
        logger = get_logger(settings)
        logger.error(f"Internal Proxy error: {exc}")
        return FastAPIJSONResponse(
            status_code=500,
            content={"error": f"IM Proxy internal error: {str(exc)}"},
        )

