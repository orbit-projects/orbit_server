"""
Orbit OpenAPI Generator

Provides OpenAPI schema generation utilities
for Orbit applications.

This module exposes the public API for:

- Route schema generation
- OpenAPI specification generation
- Request schema inspection
- Response schema inspection

Exports:
    generate_openapi_schema:
        Generate OpenAPI specification for an app.
"""

from orbit_core import App


def generate_openapi_schema(
    app: App,
) -> dict:
    """
    Generate an OpenAPI schema for an Orbit app.

    Args:
        app:
            Orbit application instance.

    Returns:
        OpenAPI specification dictionary.
    """

    paths = {}

    for route in app.get_routes():
        path = route.path

        if path not in paths:
            paths[path] = {}

        paths[path][route.method.lower()] = {
            "summary": route.handler.__name__,
            "responses": {
                "200": {
                    "description": "Successful Response",
                }
            },
        }

    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Orbit API",
            "version": "0.1.0",
        },
        "paths": paths,
    }
