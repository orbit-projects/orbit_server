"""
Orbit Server Package

Backend execution and runtime orchestration layer
for Orbit applications.

This package exposes the public API for:

- Request context handling
- Runtime execution
- Adapter integrations
- OpenAPI generation

Exports:
    RequestContext:
        Stores contextual request information during execution.
"""

from .context import RequestContext

__all__ = [
    "RequestContext",
]
