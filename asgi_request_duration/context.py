from contextvars import ContextVar

REQUEST_DURATION_CTX_KEY: str = "request_duration"
request_duration_ctx_var: ContextVar[str] = ContextVar(REQUEST_DURATION_CTX_KEY)
