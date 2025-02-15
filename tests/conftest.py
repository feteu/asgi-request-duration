import logging
import pytest
from asgi_request_duration.middleware import RequestDurationMiddleware
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


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

async def info_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "info"})

async def excluded_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "excluded"})

@pytest.fixture
def app() -> Starlette:
    routes = [
        Route("/info", info_endpoint, methods=["GET"]),
        Route("/excluded", excluded_endpoint, methods=["GET"]),
    ]
    app = Starlette(routes=routes)
    app.add_middleware(
        RequestDurationMiddleware
    )
    return app

@pytest.fixture
def valid_header_config_01() -> str:
    return "x-request-duration"

@pytest.fixture
def valid_header_config_02() -> str:
    return "X-Request-Duration"

@pytest.fixture
def valid_header_config_03() -> str:
    return "my_secpial_header"

@pytest.fixture
def invalid_header_config_01() -> str:
    return " "

@pytest.fixture
def invalid_header_config_02() -> str:
    return "$%^&*"

@pytest.fixture
def invalid_header_config_03() -> str:
    return "⚙️"

@pytest.fixture
def valid_precision_config_01() -> str:
    return 1

@pytest.fixture
def valid_precision_config_02() -> str:
    return 17

@pytest.fixture
def valid_precision_config_03() -> int:
    return 0

@pytest.fixture
def invalid_precision_config_01() -> int:
    return 7895

@pytest.fixture
def invalid_precision_config_02() -> int:
    return -1

@pytest.fixture
def invalid_precision_config_03() -> float:
    return 3.14159265358979323846