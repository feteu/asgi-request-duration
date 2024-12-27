class InvalidHeaderNameException(Exception):
    """
    Exception raised for invalid header names.
    This class represents an error that occurs when an invalid header name is provided.
    It provides a custom description to inform the user about the invalid header name.
    """
    description: str = (
        "Invalid header name provided. "
        "Please ensure that the header name is correct and try again."
    )

    def __init__(self, header_name: str, detail: str = description) -> None:
        self.header_name: str = header_name
        super().__init__(detail)

    def __str__(self) -> str:
        return f'{self.header_name} - {self.args}'

class PrecisionValueOutOfRangeException(ValueError):
    """
    Exception raised for precision values that are out of range.
    This class represents an error that occurs when a precision value is out of the allowed range.
    It provides a custom description to inform the user about the out-of-range precision value.
    """
    description: str = (
        "Precision value is out of range. "
        "Please ensure that the precision value is within the allowed range."
    )

    def __init__(self, precision: int, min_value: int, max_value: int, detail: str = description) -> None:
        self.precision: int = precision
        self.min_value: int = min_value
        self.max_value: int = max_value
        super().__init__(detail)

    def __str__(self) -> str:
        return f'{self.precision} - {self.args} (Allowed range: {self.min_value}-{self.max_value})'