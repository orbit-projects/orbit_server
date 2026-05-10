"""
Logging configuration for the Orbit application.

This module sets up a default logger named "orbit" and configures
basic logging with an INFO level.
"""

import logging

logger = logging.getLogger("orbit")
logging.basicConfig(level=logging.INFO)
