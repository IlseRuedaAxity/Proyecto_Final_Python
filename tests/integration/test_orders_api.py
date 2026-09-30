from uuid import uuid4


async def test_create_order_success(client, auth_token):
    response = await client.post(
        "/api/v1/orders",
        json={
            "customer_id": str(uuid4()),
            "customer_name": "Juan Pérez",
            "items": [
                {
                    "product_id": str(uuid4()),
                    "product_name": "Laptop",
                    "quantity": 1,
                    "unit_price": 999.99,
                }
            ],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Juan Pérez"
    assert data["status"] == "pending"
    assert data["total"] == 999.99


async def test_create_order_unauthorized(client):
    response = await client.post(
        "/api/v1/orders",
        json={"customer_id": str(uuid4()), "customer_name": "Test", "items": []},
    )
    assert response.status_code == 401


async def test_get_order_not_found(client, auth_token):
    response = await client.get(
        f"/api/v1/orders/{uuid4()}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 404


async def test_list_orders_pagination(client, auth_token):
    response = await client.get(
        "/api/v1/orders?limit=10&offset=0",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "limit" in data


async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
