import random
import time
from collections.abc import Iterator
from typing import Self

import httpx

from apiclient.models import Parcel
from apiclient.retry import RetryPolicy, get_retry_after


class ApiClient:
    def __init__(
        self,
        base_url: str,
        transport: httpx.BaseTransport | None = None,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=10.0, transport=transport)
        self._retry_policy = retry_policy or RetryPolicy()

    def get(self, path: str) -> dict:
        for attempt in range(self._retry_policy.max_retries + 1):
            try:
                response = self._client.get(path)
            except httpx.ConnectError, httpx.TimeoutException:
                if attempt == self._retry_policy.max_retries:
                    raise
                delay = self._retry_policy.get_delay(attempt + 1)
                delay += random.uniform(0, delay * 0.1)
                time.sleep(delay)
                continue
            if response.status_code == 429 or response.status_code >= 500:
                if attempt == self._retry_policy.max_retries:
                    response.raise_for_status()
                retry_after = get_retry_after(response.headers.get("Retry-After"))
                if retry_after is not None:
                    delay = retry_after
                else:
                    delay = self._retry_policy.get_delay(attempt + 1)
                    delay += random.uniform(0, delay * 0.1)
                time.sleep(delay)
                continue
            response.raise_for_status()
            return response.json()
        raise RuntimeError("Request failed after all retry attempts.")

    def paginate(self, path: str, limit: int = 100) -> Iterator[Parcel]:
        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")
        offset = 0
        seen_ids: set[int] = set()
        total = None

        while total is None or offset < total:
            separator = "&" if "?" in path else "?"
            page_path = f"{path}{separator}offset={offset}&limit={limit}"
            response = self.get(page_path)
            items = response["items"]
            total = response["total"]
            for item in items:
                parcel = Parcel.model_validate(item)
                if parcel.id not in seen_ids:
                    seen_ids.add(parcel.id)
                    yield parcel
            offset += limit

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
