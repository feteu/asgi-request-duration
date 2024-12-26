from logging import Filter, LogRecord
from asgi_request_duration.context import REQUEST_DURATION_CTX_KEY, request_duration_ctx_var

class RequestDurationFilter(Filter):
    """
    A logging filter that integrates the request duration context into log records.
    
    Attributes:
        context_key (str): The key to retrieve the request duration context value.
        default_value (str): The default value if the request duration context key is not found.
    """
    def __init__(self, name: str = "", context_key: str = REQUEST_DURATION_CTX_KEY, default_value: str = "") -> None:
        """
        Initializes the RequestDurationFilter with the given parameters.
        
        Args:
            name (str): The name of the filter.
            context_key (str): The key to retrieve the request duration context value.
            default_value (str): The default value if the request duration context key is not found.
        """
        super().__init__(name)
        self.context_key: str = context_key
        self.default_value: str = default_value

    def filter(self, record: LogRecord) -> bool:
        """
        Applies the filter to the given log record.
        
        This method retrieves the request duration context value using the context key and sets it as an attribute on the log record. If the context key is not found, the default_value is used.
        
        Args:
            record (LogRecord): The log record to which the filter is applied.
        
        Returns:
            bool: Always returns True to indicate the record should be logged.
        """
        try:
            context_value = request_duration_ctx_var.get(self.default_value)
        except RuntimeError:
            context_value = self.default_value
        setattr(record, self.context_key, context_value)
        return True