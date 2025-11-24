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

from im_connector.config import get_settings
from im_connector.fastapi_response_wrapper import FastAPIResponseWrapper
from im_connector.im_library.adapter.im_request_adapter import IMRequestAdapter
from im_connector.im_library.client.im_client import IMClient
from im_connector.logger import get_logger

settings = get_settings()

title = "IM Connector API"
summary = "IM Connector REST API"
description = "This API provides endpoints to interact with IM"
version = "0.1.0"
docs_url = "/docs"


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """FastAPI application lifespan context manager.

    This function is called at application startup and shutdown. It performs:
    - Initializes the application logger and attaches it to the request state.

    Args:
        fastapi_app: The FastAPI application instance.

    Yields:
        dict: A dictionary with the logger instance, available in the request state.

    """
    logger = get_logger(settings)
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
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# IM proxy REST interface
# All IM REST API endpoints are defined here: https://app.swaggerhub.com/apis-docs/grycap/InfrastructureManager/1.19.0

@app.api_route("/infrastructures",
               methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
               summary="Proxy interface to IM",
               description="Proxy interface to IM")
async def proxy_infrastructures_root(request: FastAPIRequest):
    """Define the route for the /infrastructure endpoint.

    This function is called when /infrastructures is called with any HTTP verb.
    The FastAPI request is received and proxied to the forward_request function

    Args:
        request: The FastAPI request
    """

    return await forward_request(request)


@app.api_route("/infrastructures/{path:path}",
               methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
               summary="Proxy interface to IM (with subpath)",
               description="Proxy interface to IM (with subpath)")
async def proxy_infrastructures_sub(request: FastAPIRequest):
    """Define the route for any sub-path of the /infrastructures endpoint.

    This function is called when any subpath of /infrastructures is called with any HTTP verb.
    The FastAPI request is received and also proxied to the forward_request function.

    Args:
        request: The FastAPI request object instance
    """

    return await forward_request(request)


@app.api_route("/clouds/{path:path}",
               methods=["GET"],
               summary="Proxy interface to IM (for /clouds endpoints)",
               description="Proxy interface to IM (for /clouds endpoints)")
async def proxy_infrastructures_sub(request: FastAPIRequest):
    """Define the route for any sub-path of the /clouds endpoint.

    This function is called when any subpath of /clouds is called with the GET HTTP verb.
    The FastAPI request is received and also proxied to the forward_request function.

    Args:
        request: The FastAPI request object instance
    """

    return await forward_request(request)


@app.api_route("/version",
               methods=["GET"],
               summary="Proxy interface to IM (for /version endpoint)",
               description="Proxy interface to IM (for /version endpoint)")
async def proxy_infrastructures_sub(request: FastAPIRequest):
    """Define the route for the /version endpoint.

    This function is called when the /version endpoint is called with the GET HTTP verb.
    The FastAPI request is received and also proxied to the forward_request function.

    Args:
        request: The FastAPI request object instance
    """

    return await forward_request(request)


@app.api_route("/stats",
               methods=["GET"],
               summary="Proxy interface to IM (for /stats endpoint)",
               description="Proxy interface to IM (for /stats endpoint)")
async def proxy_infrastructures_sub(request: FastAPIRequest):
    """Define the route for the /stats endpoint.

    This function is called when the /stats endpoint is called with the GET HTTP verb.
    The FastAPI request is received and also proxied to the forward_request function.

    Args:
        request: The FastAPI request object instance
    """

    return await forward_request(request)


@app.api_route("/oai",
               methods=["GET"],
               summary="Proxy interface to IM (for /oai endpoints)",
               description="Proxy interface to IM (for /oai endpoints)")
async def proxy_infrastructures_sub(request: FastAPIRequest):
    """Define the route for the /oai endpoint.

    This function is called when the /oai endpoint is called with the GET HTTP verb.
    The FastAPI request is received and also proxied to the forward_request function.

    Args:
        request: The FastAPI request object instance
    """

    return await forward_request(request)


async def forward_request(request: FastAPIRequest):
    """Forward the incoming request to the target InfrastructureManager deployment.

    The incoming request, received as a fastapi Request object, is parsed by the IMRequestAdapter.
    The header is disassembled and instances of objects representing the authorization credentials are created.
    Instances of objects representing the actual requests (e.g. create an infrastructure) are created.

    Header and requests objects are then passed to the IMClient.request method to be forwarded to the target IM deployment.
    The response from the IM is then converted into a fastapi Response object and returned to the caller.

    HTTP Exceptions are handled and logged.

    Args:
        request: The FastAPI request object instance.

    """

    try:
        # The body must be retrieved at this stage because the library is not async.
        request_body = await request.body()
        # An instance of the IMRequestAdapter is created passing the incoming request and the request body (i.e. the TOSCA template) .
        adapter = IMRequestAdapter(request, request_body)
        try:
            # The request and header objects are encapsulated into the IMRequestAdapter instance.
            backend_response = IMClient.request(adapter.request, adapter.header)
        except Exception as e:
            # Relaying the exception to ensure consistency with FastAPI data types.
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
