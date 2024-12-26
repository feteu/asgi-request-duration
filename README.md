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

## Table of Contents 📚

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Middleware](#middleware)
  - [Logging Filter](#logging-filter)
  - [Configuration](#configuration)
- [Examples](#examples)
- [Development](#development)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

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

### Middleware

To use the middleware, add it to your ASGI application:

```python
from asgi_request_duration.middleware import RequestDurationMiddleware
from starlette.applications import Starlette

app = Starlette()
app.add_middleware(RequestDurationMiddleware)
```

### Logging Filter

To use the logging filter, configure your logger to use the `RequestDurationFilter`:

```python
import logging
from asgi_request_duration.filters import RequestDurationFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myapp")
logger.addFilter(RequestDurationFilter())
```

### Configuration ⚙️

#### Middleware Configuration

You can configure the middleware by passing parameters to the `RequestDurationMiddleware`:

- `excluded_paths`: List of paths to exclude from timing.
- `header_name`: The name of the header to store the request duration.
- `precision`: The precision of the recorded duration.
- `skip_validate_header_name`: Flag to skip header name validation.
- `skip_validate_precision`: Flag to skip precision validation.

Example:

```python
app.add_middleware(
    RequestDurationMiddleware,
    excluded_paths=["/health"],
    header_name="X-Request-Duration",
    precision=3,
    skip_validate_header_name=False,
    skip_validate_precision=False
)
```

#### Logging Filter Configuration

You can configure the logging filter by passing parameters to the `RequestDurationFilter`:

- `context_key`: The key to retrieve the request duration context value.
- `default_value`: The default value if the request duration context key is not found.

Example:

```python
logger.addFilter(RequestDurationFilter(context_key="request_duration", default_value="-"))
```

## Examples 📖

Here are complete examples of how to use the middleware with Starlette applications. You can find the full example code in the [examples](examples) folder.

## Development 👩‍💻👨‍💻

### Requirements

- Python 3.11+
- Poetry

### Setup

Clone the repository and install the dependencies:

```sh
git clone https://github.com/yourusername/asgi-request-duration.git
cd asgi-request-duration
poetry install
```

### Running Tests 🧪

You can run the tests using `pytest`:

```sh
poetry run pytest
```

## License 📜

This project is licensed under the GNU GPLv3 License. See the [LICENSE](LICENSE) file for more details.

## Contributing 🤝

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Contact 📬

For any questions or suggestions, please open an issue on GitHub.
