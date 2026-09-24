class LoomError(Exception):
    """Base class for all Loom-specific errors."""
    pass

class LoomRuntimeError(LoomError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class LoomLexerError(LoomError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class LoomParseError(LoomError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
