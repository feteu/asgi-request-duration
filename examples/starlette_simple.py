import uvicorn
from asgi_request_duration import RequestDurationMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route('/')
async def homepage(request) -> JSONResponse:
    return JSONResponse({'message': 'Hello, world!'})

app.add_middleware(RequestDurationMiddleware)

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)