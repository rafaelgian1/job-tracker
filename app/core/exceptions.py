from fastapi.responses import JSONResponse


class AuthError(Exception):
    def __init__(self, *, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"{self.message}, Error code: {self.error_code}"


def handle_exceptions(request, exc):
    return JSONResponse(
        status_code=exc.error_code,
        content={"detail": exc.message},
    )
