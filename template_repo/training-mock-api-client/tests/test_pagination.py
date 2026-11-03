import httpx

from apiclient.client import ApiClient


def test_pagination_returns_all_items_without_duplicates():
    pages = {
        0: {
            "items": [
                {
                    "id": 1,
                    "name": "Birch 0001",
                    "status": "active",
                    "category": "charlie",
                    "created": "2026-09-08",
                },
                {
                    "id": 2,
                    "name": "Dune 0002",
                    "status": "active",
                    "category": "standard",
                    "created": "2026-09-07",
                },
                {
                    "id": 3,
                    "name": "Birch 0003",
                    "status": "active",
                    "category": "hardware",
                    "created": "2026-09-10",
                },
            ],
            "offset": 0,
            "limit": 3,
            "total": 5,
        },
        3: {
            "items": [
                {
                    "id": 3,
                    "name": "Birch 0003",
                    "status": "active",
                    "category": "hardware",
                    "created": "2026-09-10",
                },
                {
                    "id": 4,
                    "name": "Atlas 0004",
                    "status": "active",
                    "category": "standard",
                    "created": "2026-09-07",
                },
                {
                    "id": 5,
                    "name": "Iris 0005",
                    "status": "active",
                    "category": "charlie",
                    "created": "2026-09-08",
                },
            ],
            "offset": 3,
            "limit": 3,
            "total": 5,
        },
    }

    def handler(request: httpx.Request) -> httpx.Response:
        offset = int(request.url.params["offset"])
        return httpx.Response(200, json=pages[offset])

    transport = httpx.MockTransport(handler)

    with ApiClient(base_url="http://test", transport=transport) as client:
        items = list(client.paginate("/v1/parcels", limit=3))
    assert [item.id for item in items] == [1, 2, 3, 4, 5]
