[![PyPI - Downloads](https://img.shields.io/pypi/dm/asgi-request-duration.svg)](https://pypi.org/project/asgi-request-duration/)
[![PyPI - License](https://img.shields.io/pypi/l/asgi-request-duration)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI - Version](https://img.shields.io/pypi/v/asgi-request-duration.svg)](https://pypi.org/project/asgi-request-duration/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asgi-request-duration)](https://pypi.org/project/asgi-request-duration/)
[![PyPI - Status](https://img.shields.io/pypi/status/asgi-request-duration)](https://pypi.org/project/asgi-request-duration/)
[![Dependencies](https://img.shields.io/librariesio/release/pypi/asgi-request-duration)](https://libraries.io/pypi/asgi-request-duration)
[![Last Commit](https://img.shields.io/github/last-commit/feteu/asgi-request-duration)](https://github.com/feteu/asgi-request-duration/commits/main)
[![Build Status build/testpypi](https://img.shields.io/github/actions/workflow/status/feteu/asgi-request-duration/publish-testpypi.yaml?label=publish-testpypi)](https://github.com/feteu/asgi-request-duration/actions/workflows/publish-testpypi.yaml)
[![Build Status build/pypi](https://img.shields.io/github/actions/workflow/status/feteu/asgi-request-duration/publish-pypi.yaml?label=publish-pypi)](https://github.com/feteu/asgi-request-duration/actions/workflows/publish-pypi.yaml)
[![Build Status test](https://img.shields.io/github/actions/workflow/status/feteu/asgi-request-duration/test.yaml?label=test)](https://github.com/feteu/asgi-request-duration/actions/workflows/test.yaml)

# ASGI Request Duration ⏱️

ASGI Request Duration is a middleware for ASGI applications that measures the duration of HTTP requests and integrates this information into response headers and log records. This middleware is designed to be easy to integrate and configure, providing valuable insights into the performance of your ASGI application.

> **Note:** If you find this project useful, please consider giving it a star ⭐ on GitHub. This helps prioritize its maintenance and development. If you encounter any typos, bugs 🐛, or have new feature requests, feel free to open an issue. I will be happy to address them.

## Table of Contents 📚

1. [Features ✨](#features-✨)
2. [Installation 🛠️](#installation-🛠️)
3. [Usage 🚀](#usage-🚀)
    1. [Middleware 🧩](#middleware-🧩)
    2. [Logging Filter 📝](#logging-filter-📝)
    3. [Configuration ⚙️](#configuration-⚙️)
      1. [Middleware Configuration 🔧](#middleware-configuration-🔧)
      2. [Logging Filter Configuration 🔍](#logging-filter-configuration-🔍)
4. [Examples 📖](#examples-📖)
    1. [Example with Starlette 🌟](#example-with-starlette-🌟)
5. [Contributing 🤝](#contributing-🤝)
6. [License 📜](#license-📜)

## Features ✨

- Measure the duration of each HTTP request.
- Add the request duration to response headers.
- Integrate the request duration into log records.
- Configurable header name and precision.
- Exclude specific paths from timing.

## Installation 🛠️

You can install the package using pip:

```bash
pip install asgi-request-duration
```

## Usage 🚀

### Middleware 🧩

To use the middleware, add it to your ASGI application:

```python
from asgi_request_duration.middleware import RequestDurationMiddleware
from starlette.applications import Starlette

app = Starlette()
app.add_middleware(RequestDurationMiddleware)
```

### Logging Filter 📝

To use the logging filter, configure your logger to use the `RequestDurationFilter`:

```python
import logging
from asgi_request_duration.filters import RequestDurationFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myapp")
logger.addFilter(RequestDurationFilter())
```

### Configuration ⚙️

#### Middleware Configuration 🔧

You can configure the middleware by passing parameters to the `RequestDurationMiddleware`:

- `excluded_paths`: List of paths to exclude from timing.
- `header_name`: The name of the header to store the request duration.
- `precision`: The precision of the recorded duration.
- `skip_validate_header_name`: Flag to skip header name validation.
- `skip_validate_precision`: Flag to skip precision validation.
- `time_granularity`: Specifies the unit of time measurement (default: `Seconds`).

Example:

```python
app.add_middleware(
    RequestDurationMiddleware,
    excluded_paths=["^/health/?$"],
    header_name="x-request-duration",
    precision=3,
    skip_validate_header_name=False,
    skip_validate_precision=False,
    time_granularity=TimeGranularity.MILLISECONDS,
)
```

#### Logging Filter Configuration 🔍

You can configure the logging filter by passing parameters to the `RequestDurationFilter`:

- `context_key`: The key to retrieve the request duration context value.
- `default_value`: The default value if the request duration context key is not found.

Example:

```python
logger.addFilter(RequestDurationFilter(context_key="request_duration", default_value="-"))
```

## Examples 📖

Here is a complete example of how to use the middleware with the Starlette framework. For more examples and detailed usage, please refer to the [examples](https://github.com/feteu/asgi-request-duration/tree/main/examples) folder in the repository.

### Example with Starlette 🌟

```python
from asgi_request_duration import RequestDurationMiddleware, TimeGranularity
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
    time_granularity=TimeGranularity.MILLISECONDS,
)

if __name__ == "__main__":
    run(app, host='127.0.0.1', port=8000)
```

## Contributing 🤝
Contributions are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License 📜
This project is licensed under the GNU GPLv3 License. See the [LICENSE](LICENSE) file for more details.
