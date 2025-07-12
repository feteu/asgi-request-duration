import logging
import re
import time
from dataclasses import dataclass, field
from starlette.datastructures import MutableHeaders, URL
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from .context import request_duration_ctx_var
from .decorators import validate_header_name, validate_precision
from .constants import (
    _DEFAULT_EXCLUDED_PATHS,
    _DEFAULT_HEADER_NAME,
    _DEFAULT_PRECISION,
    _DEFAULT_SKIP_VALIDATE_HEADER_NAME,
    _DEFAULT_SKIP_VALIDATE_PRECISION,
    _DEFAULT_TIME_GRANULARITY,
)
from .enums import TimeGranularity

log = logging.getLogger(__name__)

@dataclass
class RequestDurationMiddleware:
    """
    Middleware to measure and record the duration of HTTP requests.

    Attributes:
        app (ASGIApp): The ASGI application.
        excluded_paths_patterns (list[re.Pattern]): Compiled regex patterns for paths to exclude from timing.
        excluded_paths (list[str | None]): List of paths to exclude from timing.
        header_name (str): The name of the header to store the request duration.
        precision (int): Number of decimal places for the recorded duration value.
        skip_validate_header_name (bool): If True, skips header name validation.
        skip_validate_precision (bool): If True, skips precision value validation.
        time_granularity (TimeGranularity): Specifies the unit for the recorded duration value. Can be:
            - TimeGranularity.SECONDS (default): duration in seconds
            - TimeGranularity.MILLISECONDS: duration in milliseconds
            - TimeGranularity.MICROSECONDS: duration in microseconds
            - TimeGranularity.NANOSECONDS: duration in nanoseconds
    """
    app: ASGIApp
    excluded_paths_patterns: list[re.Pattern] = field(init=False)
    excluded_paths: list[str | None] = field(default_factory=lambda: _DEFAULT_EXCLUDED_PATHS)
    header_name: str = _DEFAULT_HEADER_NAME
    precision: int = _DEFAULT_PRECISION
    skip_validate_header_name: bool = _DEFAULT_SKIP_VALIDATE_HEADER_NAME
    skip_validate_precision: bool = _DEFAULT_SKIP_VALIDATE_PRECISION
    time_granularity: TimeGranularity = _DEFAULT_TIME_GRANULARITY

    @validate_header_name(skip=skip_validate_header_name)
    @validate_precision(skip=skip_validate_precision)
    def __post_init__(self) -> None:
        """
        Post-initialization to compile excluded path patterns and validate attributes.
        """
        self.excluded_paths_patterns = [re.compile(e) for e in self.excluded_paths]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        ASGI callable to handle the request and measure its duration.
        
        Args:
            scope (Scope): The ASGI scope.
            receive (Receive): The ASGI receive callable.
            send (Send): The ASGI send callable.
        """
        if scope["type"] not in ("http",):
            await self.app(scope, receive, send)
            return
        
        time_recording_start = time.perf_counter()
        url = URL(scope=scope)
        
        if self._search_patterns_in_string(url.path, self.excluded_paths_patterns):
            await self.app(scope, receive, send)
            return
        
        async def wrapped_send(message: Message) -> None:
            """
            Wrapper for the send callable to add the request duration header.
            
            Args:
                message (Message): The ASGI message.
            """
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                request_duration_ctx_var.set(
                    f"{(time.perf_counter() - time_recording_start) * self.time_granularity.value:.{self.precision}f}"
                )
                headers.append(self.header_name, request_duration_ctx_var.get())
            await send(message)
        
        await self.app(scope, receive, wrapped_send)

    @staticmethod
    def _search_patterns_in_string(s: str, patterns: list[re.Pattern]) -> bool:
        """
        Search for any pattern in the string.
        
        Args:
            s (str): The string to search.
            patterns (list[re.Pattern]): The list of compiled regex patterns.
        
        Returns:
            bool: True if any pattern matches the string. False otherwise.
        """
        return any(p.search(s) for p in patterns)