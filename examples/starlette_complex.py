from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from asgi_request_duration import RequestDurationMiddleware
import uvicorn

async def homepage(request) -> JSONResponse:
    return JSONResponse({'message': 'Hello, world!'})

async def about(request) -> JSONResponse:
    return JSONResponse({'message': 'About page'})

async def contact(request) -> JSONResponse:
    return JSONResponse({'message': 'Contact page'})

routes = [
    Route("/", endpoint=homepage),
    Route("/about", endpoint=about),
    Route("/contact", endpoint=contact),
]

config = {
    'header_name': 'X-Request-Duration-Starlette-Complex',
    'precision': 17,
    'excluded_paths': ['/about', '/contact'],
    'skip_validate_header_name': False,
    'skip_validate_precision': True
}

middleware = [
    Middleware(
        RequestDurationMiddleware,
        **config
    )
]

app = Starlette(routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)