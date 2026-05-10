"""
Public API for the server module.

This module exposes the main application factory function
used to create a Starlette app instance.
"""

from .server import create_starlette_app

__all__ = ["create_starlette_app"]
