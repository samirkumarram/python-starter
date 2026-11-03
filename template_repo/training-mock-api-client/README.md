**# Traing Mock API Client**

A reusable Python client for interacting with the Training Mock API.

## **Features**

1. HTTP GET requests using HTTPX.
2. Configurable request timeout.
3. Automatic retries for HTTP 429 and 5xx responses.
4. Exponential backoff with jitter.
5. Supports the Retry-After response header.
6. Pagination support.
7. Duplicate parcel removal using parcel IDs.
8. Pydantic validation of parcel records.

## **Requirements**

1. Python 3.14 or later
2. uv

## **Installation**

uv sync

## **Running Tests**

uv run pytest -v