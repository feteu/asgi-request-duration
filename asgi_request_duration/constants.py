import re

_DEFAULT_EXCLUDED_PATHS = []
_DEFAULT_HEADER_NAME = "X-Request-Duration"
_DEFAULT_PRECISION = 6
_DEFAULT_SKIP_VALIDATE_HEADER_NAME = False
_DEFAULT_SKIP_VALIDATE_PRECISION = False
_HEADER_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-_]*$")
_PRECISION_MAX = 17
_PRECISION_MIN = 0
