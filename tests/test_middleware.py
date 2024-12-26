from starlette.testclient import TestClient
from starlette.applications import Starlette


def test_request_duration_header(asgi_app_with_middleware: Starlette) -> None:
    with TestClient(asgi_app_with_middleware) as client:
        response = client.get("/")
        assert "X-Request-Duration" in response.headers
        duration = response.headers["X-Request-Duration"]
        assert duration.replace(".", "").isdigit()

def test_excluded_path(asgi_app_with_middleware: Starlette) -> None:
    with TestClient(asgi_app_with_middleware) as client:
        response = client.get("/exclude")
        assert "X-Request-Duration" not in response.headers

def test_precision(asgi_app_with_middleware: Starlette) -> None:
    with TestClient(asgi_app_with_middleware) as client:
        response = client.get("/")
        duration = response.headers.get("X-Request-Duration")
        assert duration is not None
        assert len(duration.split(".")[1]) <= 6
