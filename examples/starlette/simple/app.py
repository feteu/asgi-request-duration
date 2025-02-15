from asgi_request_duration import RequestDurationMiddleware
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from uvicorn import run


async def info_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "info"})

async def excluded_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({"message": "excluded"})

routes = [
    Route("/info", info_endpoint, methods=["GET"]),
    Route("/excluded", excluded_endpoint, methods=["GET"]),
]

app = Starlette(routes=routes)
app.add_middleware(
    RequestDurationMiddleware,
    excluded_paths=["/excluded"],
    header_name="x-request-duration",
    precision=4,
    skip_validate_header_name=False,
    skip_validate_precision=False,
)

if __name__ == "__main__":
    run(app, host='127.0.0.1', port=8000)