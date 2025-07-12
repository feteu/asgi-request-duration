import pytest
import re
from httpx import AsyncClient, ASGITransport
from starlette.applications import Starlette
from asgi_request_duration.constants import TimeGranularity


async def test_middleware_info_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert float(response.headers.get("x-request-duration"))

async def test_middleware_excluded_endpoint(app: Starlette) -> None:
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/excluded")
        assert response.status_code == 200
        assert response.json() == {"message": "excluded"}
        assert float(response.headers.get("x-request-duration"))

async def test_middleware_excluded_endpoint_with_valid_excluded_path(app: Starlette) -> None:
    app.user_middleware[0].kwargs["excluded_paths"] = ["^/excluded/?$"]
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/excluded")
        assert response.status_code == 200
        assert response.json() == {"message": "excluded"}
        assert response.headers.get("x-request-duration") == None

async def test_middleware_excluded_endpoint_with_invalid_excluded_path(app: Starlette) -> None:
    app.user_middleware[0].kwargs["excluded_paths"] = ["^/invalid_path/?$"]
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/excluded")
        assert response.status_code == 200
        assert response.json() == {"message": "excluded"}
        assert float(response.headers.get("x-request-duration"))

async def test_middleware_excluded_endpoint_with_valid_header_name(app: Starlette) -> None:
    app.user_middleware[0].kwargs["header_name"] = "x-my-company-request-duration"
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert float(response.headers.get("x-my-company-request-duration"))

async def test_middleware_excluded_endpoint_with_valid_precision(app: Starlette) -> None:
    app.user_middleware[0].kwargs["precision"] = 10
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert re.match(r"^[0-9]+\.[0-9]{10}$", response.headers.get("x-request-duration"))

@pytest.mark.parametrize("time_granularity", [f"valid_time_granularity_config_{i:02d}" for i in range(1, 5)])
async def test_middleware_excluded_endpoint_with_valid_time_granularity(app: Starlette, time_granularity: TimeGranularity, request: pytest.FixtureRequest) -> None:
    app.user_middleware[0].kwargs["time_granularity"] = request.getfixturevalue(time_granularity)
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/info")
        assert response.status_code == 200
        assert response.json() == {"message": "info"}
        assert re.match(r"^[0-9]+\.[0-9].+$", response.headers.get("x-request-duration"))