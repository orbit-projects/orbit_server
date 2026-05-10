"""
Starlette adapter for Orbit applications.

This module provides a function to convert an Orbit App instance
into a Starlette ASGI application, including route handling,
middleware execution, error handling, and OpenAPI documentation.
"""

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse, HTMLResponse

from orbit_core import App
from .executor import execute_handler
from .adapters import parse_request, to_response, error_response
from .context import RequestContext

from .openapi import generate_openapi

import traceback


def create_starlette_app(orbit_app: App):
    """
    Create a Starlette application from an Orbit app instance.

    This function maps Orbit routes to Starlette routes, wraps handlers
    with middleware, and sets up OpenAPI and documentation endpoints.

    Args:
        orbit_app (App): The Orbit application instance.

    Returns:
        Starlette: A configured Starlette ASGI application.
    """
    routes = []

    for route_def in orbit_app.get_routes():

        async def endpoint(request, route_def=route_def):
            """
            Handle an incoming HTTP request for a specific route.

            This function builds the request context, executes middleware,
            calls the route handler, and converts the result into a response.

            Args:
                request: The incoming Starlette request.

            Returns:
                Response: A Starlette response object.
            """
            context = RequestContext(request)
            request_cache = {}

            async def call_handler():
                """
                Execute the route handler with parsed request data
                and dependency injection.
                """
                data = await parse_request(request)

                return await execute_handler(
                    route_def.handler,
                    data,
                    container=orbit_app.container,
                    request_cache=request_cache,
                    context=context,
                )

            handler = call_handler

            for middleware in reversed(orbit_app.middlewares):
                next_handler = handler

                def make_wrapper(middleware, next_handler):
                    """
                    Wrap a handler with middleware.

                    Args:
                        middleware: The middleware function.
                        next_handler: The next handler in the chain.

                    Returns:
                        Callable: A wrapped async handler.
                    """
                    async def wrapper():
                        print("MIDDLEWARE:", middleware, type(middleware))
                        print("NEXT_HANDLER:", next_handler, type(next_handler))

                        return await middleware(context, next_handler)
                    return wrapper

                handler = make_wrapper(middleware, next_handler)

            try:
                result = await handler()
                return to_response(result)

            except Exception as e:
                traceback.print_exc()
                return error_response(e, debug=orbit_app.debug)

        routes.append(
            Route(
                path=route_def.path,
                endpoint=endpoint,
                methods=[route_def.method],
            )
        )

    async def openapi_endpoint(request):
        """
        Serve the OpenAPI schema as JSON.

        Args:
            request: The incoming Starlette request.

        Returns:
            JSONResponse: The OpenAPI specification.
        """
        schema = generate_openapi(orbit_app)
        return JSONResponse(schema)

    async def docs_endpoint(request):
        """
        Serve Swagger UI documentation.

        Args:
            request: The incoming Starlette request.

        Returns:
            HTMLResponse: Swagger UI HTML page.
        """
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Orbit Docs</title>
            <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
                SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui'
                });
            </script>
        </body>
        </html>
        """
        return HTMLResponse(html)

    routes.append(Route("/openapi.json", openapi_endpoint, methods=["GET"]))
    routes.append(Route("/docs", docs_endpoint, methods=["GET"]))

    return Starlette(routes=routes)
