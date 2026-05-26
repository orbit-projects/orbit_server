"""
Orbit Logging System

Provides shared logging utilities used throughout
the Orbit runtime.

This module exposes the public API for:

- Runtime logging
- Debug logging
- Structured framework logs
- Server lifecycle logging

Exports:
    logger:
        Shared Orbit logger instance.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format=("[Orbit] " "%(levelname)s " "%(asctime)s " "%(message)s"),
)

logger = logging.getLogger("orbit")
