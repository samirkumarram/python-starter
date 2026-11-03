from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime


@dataclass(frozen=True)
class RetryPolicy:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0

    def get_delay(self, retry_number: int) -> float:
        delay = self.base_delay * (2 ** (retry_number - 1))
        return min(delay, self.max_delay)


def get_retry_after(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            retry_date = parsedate_to_datetime(value)
        except TypeError, ValueError, OverflowError:
            return None
        if retry_date.tzinfo is None:
            retry_date = retry_date.replace(tzinfo=UTC)
        remaining = (retry_date - datetime.now(UTC)).total_seconds()
        return max(0.0, remaining)
