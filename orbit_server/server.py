"""
Orbit Runtime Server

Provides the primary runtime orchestration layer
for Orbit applications.

This module exposes the public API for:

- Runtime bootstrapping
- Adapter lifecycle management
- Route initialization
- Application execution

Exports:
    OrbitServer:
        Main Orbit runtime server.
"""

from orbit_core import App

from .adapters import BaseAdapter
from .logger import logger


class OrbitServer:
    """
    Main Orbit runtime server.

    The Orbit server coordinates:
    - Application runtime lifecycle
    - Adapter initialization
    - Runtime startup
    - Route registration
    """

    def __init__(
        self,
        app: App,
        adapter: BaseAdapter,
    ):
        """
        Initialize Orbit server.

        Args:
            app:
                Orbit application instance.

            adapter:
                Runtime adapter implementation.
        """

        self.app = app
        self.adapter = adapter

    async def start(self) -> None:
        """
        Start the Orbit runtime server.
        """

        logger.info(
            "Starting Orbit server with %s routes",
            len(self.app.get_routes()),
        )

        await self.adapter.start()
