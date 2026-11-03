import httpx

from apiclient.client import ApiClient


def test_get_retries_after_server_error() -> None:
    attempts = 0

    def fake_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1

        if attempts == 1:
            return httpx.Response(status_code=500, json={"detail": "Server error."})
        return httpx.Response(status_code=200, json={"status": "success"})

    transport = httpx.MockTransport(fake_handler)
    with ApiClient(base_url="http://test-api", transport=transport) as client:
        result = client.get("/parcels")
    assert attempts == 2
    assert result == {"status": "success"}


def test_get_respects_retry_after_header(monkeypatch) -> None:
    attempts = 0
    delays = []

    def fake_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(status_code=429, headers={"Retry-After": "2"})
        return httpx.Response(status_code=200, json={"status": "success"})

    monkeypatch.setattr("apiclient.client.time.sleep", delays.append)
    transport = httpx.MockTransport(fake_handler)
    with ApiClient(base_url="http://test-api", transport=transport) as client:
        result = client.get("/parcels")
    assert result == {"status": "success"}
    assert attempts == 2
    assert delays == [2.0]


def test_get_does_not_retry_not_found() -> None:
    attempts = 0

    def fake_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(status_code=404, json={"detail": "Parcel not found."})

    transport = httpx.MockTransport(fake_handler)
    with ApiClient(base_url="http:test-api", transport=transport) as client:
        try:
            client.get("/parcels/999")
        except httpx.HTTPStatusError as err:
            assert err.response.status_code == 404
        else:
            raise AssertionError("Expected HTTPStatusError")
    assert attempts == 1


def test_get_stops_after_maximum_retries(monkeypatch) -> None:
    attempts = 0

    def fake_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        return httpx.Response(status_code=500, json={"detail": "Server error."})

    monkeypatch.setattr("apiclient.client.time.sleep", lambda delay: None)

    transport = httpx.MockTransport(fake_handler)

    with ApiClient(base_url="http://test-api", transport=transport) as client:
        try:
            client.get("/parcels")
        except httpx.HTTPStatusError as err:
            assert err.response.status_code == 500
        else:
            raise AssertionError("Expected HTTPStatusError")
    assert attempts == 4


def test_get_retries_connection_error(monkeypatch) -> None:
    attempts = 0

    def fake_handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise httpx.ConnectError("Connection failed!")
        return httpx.Response(status_code=200, json={"status": "success"})

    monkeypatch.setattr("apiclient.client.time.sleep", lambda delay: None)

    transport = httpx.MockTransport(fake_handler)

    with ApiClient(base_url="http://test-api", transport=transport) as client:
        result = client.get("/parcels")

    assert attempts == 2
    assert result == {"status": "success"}
