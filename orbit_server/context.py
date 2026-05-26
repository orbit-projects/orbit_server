"""
Orbit Request Context

Provides request-scoped execution state used
throughout the Orbit runtime.

This module exposes the public API for:

- Request-scoped state
- Dependency cache storage
- Execution metadata
- Shared request context handling

Exports:
    RequestContext:
        Stores request-scoped execution data.
"""

from orbit_types import RequestModel


class RequestContext:
    """
    Represents request-scoped execution state.

    The request context is shared across middleware,
    handlers, and runtime execution systems during
    a request lifecycle.

    Attributes:
        request:
            Incoming normalized request model.

        request_cache:
            Request-scoped dependency cache.

        state:
            Shared mutable request state.
    """

    def __init__(
        self,
        request: RequestModel,
    ):
        """
        Initialize request context.

        Args:
            request:
                Incoming request model.
        """

        self.request = request

        self.request_cache: dict = {}
        self.state: dict = {}

    def set(
        self,
        key: str,
        value,
    ) -> None:
        """
        Store request-scoped state.

        Args:
            key:
                State key.

            value:
                State value.
        """

        self.state[key] = value

    def get(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve request-scoped state.

        Args:
            key:
                State key.

            default:
                Fallback value.

        Returns:
            Stored state value.
        """

        return self.state.get(key, default)
