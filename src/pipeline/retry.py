import time
from typing import Callable, TypeVar

T = TypeVar("T")


def with_retry(fn: Callable[[], T], attempts: int = 3, backoff: float = 1.5) -> T:
    """Run fn, retrying on any exception with exponential backoff.

    Used only for network calls (SerpApi, web3 RPC): the calls that can fail
    transiently. Not for local DeepFace calls, which don't have that failure
    mode.
    """
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            if attempt < attempts:
                time.sleep(backoff**attempt)
    assert last_exc is not None
    raise last_exc
