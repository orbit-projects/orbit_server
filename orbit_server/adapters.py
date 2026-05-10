from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from orbit_types.exceptions import OrbitError
from orbit_types import ResponseModel


async def parse_request(request: Request):
    """
    Parse the incoming HTTP request body as JSON.

    Args:
        request (Request): The incoming Starlette request object.

    Returns:
        dict: Parsed JSON body if successful, otherwise an empty dictionary.
    """
    try:
        return await request.json()
    except Exception:
        return {}


def to_response(result):
    """
    Convert a handler result into a Starlette Response.

    This function standardizes different return types into a proper HTTP response.

    Args:
        result: The result returned by a route handler.

    Returns:
        Response: A Starlette response object.
    """
    if isinstance(result, Response):
        return result

    if isinstance(result, ResponseModel):
        return JSONResponse(result.to_dict())

    if isinstance(result, dict):
        return JSONResponse(result)

    return JSONResponse({"data": result})


def error_response(error: Exception, debug=False):
    """
    Generate a standardized error response.

    Args:
        error (Exception): The exception that occurred.
        debug (bool): Whether to include detailed error messages.

    Returns:
        JSONResponse: A formatted error response with appropriate status code.
    """
    if isinstance(error, OrbitError):
        return JSONResponse(
            {
                "error": "validation_error",
                "details": format_validation_errors(error.args[0])
            },
            status_code=400,
        )

    return JSONResponse(
        {
            "error": "internal_server_error",
            "message": str(error) if debug else "Something went wrong",
        },
        status_code=500,
    )


def format_validation_errors(errors):
    """
    Format validation errors into a standardized structure.

    Args:
        errors (list): A list of validation error dictionaries.

    Returns:
        list: A list of formatted error objects containing field, message, and type.
    """
    return [
        {
            "field": ".".join(map(str, e["loc"])),
            "message": e["msg"],
            "type": e["type"],
        }
        for e in errors
    ]
