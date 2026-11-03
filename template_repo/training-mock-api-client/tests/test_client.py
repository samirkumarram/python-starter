import httpx

from apiclient.client import ApiClient


def test_get_returns_json_reponse() -> None:
    def fake_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200, json={"status": "success", "message": "API is working properly."}
        )

    transport = httpx.MockTransport(fake_handler)

    with ApiClient(base_url="http://test-api", transport=transport) as client:
        result = client.get("/health")

    assert result == {"status": "success", "message": "API is working properly."}


def test_det_raises_error_for_server_failure() -> None:
    def fake_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=500, json={"detail": "Internal Server Error"})

    transport = httpx.MockTransport(fake_handler)

    with ApiClient(base_url="http://test-api", transport=transport) as client:
        try:
            client.get("/parcels")
        except httpx.HTTPStatusError as error:
            assert error.response.status_code == 500
        else:
            raise AssertionError("Expected HTTPStatusError")
