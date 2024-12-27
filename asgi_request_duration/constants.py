import re

_DEFAULT_EXCLUDED_PATHS: list = []
_DEFAULT_HEADER_NAME: str = "X-Request-Duration"
_DEFAULT_PRECISION: int = 6
_DEFAULT_SKIP_VALIDATE_HEADER_NAME: bool = False
_DEFAULT_SKIP_VALIDATE_PRECISION: bool = False
_HEADER_NAME_PATTERN: re.Pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-_]*$")
_PRECISION_MAX: int = 17
_PRECISION_MIN: int = 0
