import logging
import pytest
from asgi_request_duration.middleware import RequestDurationMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse


@pytest.fixture
def log_record() -> logging.LogRecord:
    return logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test log message",
        args=(),
        exc_info=None
    )

@pytest.fixture
def middleware_config() -> dict[str, object]:
    return {
        "header_name": "X-Request-Duration",
        "precision": 6,
        "excluded_paths": ["/exclude"],
        "skip_validate_header_name": False,
        "skip_validate_precision": False
    }

@pytest.fixture
def asgi_app_with_middleware(middleware_config: dict[str, object]) -> Starlette:
    app = Starlette(
        middleware=[
            Middleware(RequestDurationMiddleware, **middleware_config)
        ]
    )

    async def homepage(request) -> JSONResponse:
        return JSONResponse({"message": "Hello, world!"})

    async def exclude(request) -> JSONResponse:
        return JSONResponse({"message": "This path is excluded"})

    app.add_route("/", homepage)
    app.add_route("/exclude", exclude)

    return app
