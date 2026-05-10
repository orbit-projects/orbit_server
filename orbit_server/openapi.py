import inspect

def generate_openapi(app):
    """
    Generate an OpenAPI specification from the application's routes.

    This function iterates over all registered routes in the app and constructs
    an OpenAPI 3.0-compliant schema including paths, methods, request bodies,
    and response schemas (if available).

    Args:
        app: The application instance that provides a `get_routes()` method.

    Returns:
        dict: A dictionary representing the OpenAPI specification.
    """
    paths = {}

    for route in app.get_routes():
        path = route.path
        method = route.method.lower()

        if path not in paths:
            paths[path] = {}

        paths[path][method] = {
            "summary": route.handler.__name__,
            "responses": {
                "200": {
                    "description": "Successful Response"
                }
            }
        }

        if (
            route.request_model
            and route.request_model != inspect._empty
            and hasattr(route.request_model, "model_json_schema")
        ):
            paths[path][method]["requestBody"] = {
                "content": {
                    "application/json": {
                        "schema": route.request_model.model_json_schema()
                    }
                }
            }

        if (
            route.response_model
            and route.response_model != inspect._empty
            and hasattr(route.response_model, "model_json_schema")
        ):
            paths[path][method]["responses"]["200"]["content"] = {
                "application/json": {
                    "schema": route.response_model.model_json_schema()
                }
            }

    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Orbit API",
            "version": "1.0.0"
        },
        "paths": paths
    }
