from functools import wraps
import threading


class RecursionDetected(RuntimeError):
    """function has been detected to be recursing"""


def not_recursive(f):
    """
    raise an exception if recursive
    """
    local_storage = threading.local()

    @wraps(f)
    def wrapper(*args, **kwargs):
        if getattr(local_storage, "running", False):
            raise RecursionDetected(f"function '{f.__name__}' is recursive")

        local_storage.running = True
        try:
            return f(*args, **kwargs)
        finally:
            local_storage.running = False

    return wrapper
