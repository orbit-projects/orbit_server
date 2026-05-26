"""
Orbit Request Executor

Provides handler execution utilities used throughout
the Orbit runtime.

This module exposes the public API for:

- Route handler execution
- Async handler support
- Response normalization
- Exception handling
- Dependency injection integration

Exports:
    execute_handler:
        Execute an Orbit route handler.
"""

import inspect
from typing import Any

from orbit_core import RouteDefinition
from orbit_types import (
    ExecutionError,
    RequestModel,
    ResponseModel,
)


async def execute_handler(
    route: RouteDefinition,
    request: RequestModel,
) -> ResponseModel:
    """
    Execute a route handler.

    Args:
        route:
            Registered route definition.

        request:
            Incoming request model.

    Returns:
        Normalized response model.

    Raises:
        ExecutionError:
            Raised when handler execution fails.
    """

    handler = route.handler

    try:
        kwargs = {}

        if route.request_model is not None:
            kwargs["request"] = request

        if inspect.iscoroutinefunction(handler):
            result = await handler(**kwargs)
        else:
            result = handler(**kwargs)

        return normalize_response(result)

    except Exception as exc:
        raise ExecutionError(f"Handler execution failed: {exc}") from exc


def normalize_response(
    value: Any,
) -> ResponseModel:
    """
    Normalize handler output into a response model.

    Args:
        value:
            Raw handler output.

    Returns:
        Normalized response model.
    """

    if isinstance(value, ResponseModel):
        return value

    return ResponseModel(
        body=value,
    )
