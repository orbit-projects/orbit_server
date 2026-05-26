"""
Orbit Adapter System

Provides backend adapter abstractions used to connect
Orbit applications to external runtimes.

This module exposes the public API for:

- Runtime adapters
- Request conversion
- Response conversion
- Backend integration

Exports:
    BaseAdapter:
        Base adapter abstraction for Orbit runtimes.
"""

from abc import ABC
from abc import abstractmethod

from orbit_core import App
from orbit_types import (
    RequestModel,
    ResponseModel,
)


class BaseAdapter(ABC):
    """
    Base runtime adapter abstraction.

    Adapters are responsible for translating
    external runtime behavior into Orbit-compatible
    request and response models.
    """

    def __init__(
        self,
        app: App,
    ):
        """
        Initialize adapter.

        Args:
            app:
                Orbit application instance.
        """

        self.app = app

    @abstractmethod
    async def handle_request(
        self,
        request: RequestModel,
    ) -> ResponseModel:
        """
        Handle an incoming request.

        Args:
            request:
                Normalized request model.

        Returns:
            Normalized response model.
        """

    @abstractmethod
    async def start(self) -> None:
        """
        Start adapter runtime.
        """
