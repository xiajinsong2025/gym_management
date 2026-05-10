def test_member_card_order_flow(test_client):
    register_response = test_client.post(
        "/api/v1/auth/register",
        json={"username": "admin", "password": "123456", "display_name": "Admin"},
    )
    assert register_response.status_code == 200
    login_response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "123456"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    grant_response = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["transactions:read", "transactions:write", "members:write"]},
        headers=headers,
    )
    assert grant_response.status_code == 200

    create_member_response = test_client.post(
        "/api/v1/members",
        json={"name": "Alice", "mobile": "13800000001", "member_no": "M1001"},
        headers=headers,
    )
    assert create_member_response.status_code == 200
    member_id = create_member_response.json()["data"]["id"]

    create_card_type_response = test_client.post(
        "/api/v1/card-types",
        json={"name": "Stored Value", "kind": "stored_value", "price_cents": 10000},
        headers=headers,
    )
    assert create_card_type_response.status_code == 200
    card_type_id = create_card_type_response.json()["data"]["id"]

    open_card_response = test_client.post(
        "/api/v1/member-cards/open",
        json={
            "member_id": member_id,
            "card_type_id": card_type_id,
            "card_no": "C1001",
            "balance_cents": 10000,
            "total_amount_cents": 10000,
        },
        headers=headers,
    )
    assert open_card_response.status_code == 200
    card_data = open_card_response.json()["data"]
    assert card_data["status"] == "active"
    assert card_data["balance_cents"] == 10000
    card_id = card_data["id"]

    recharge_response = test_client.post(
        f"/api/v1/member-cards/{card_id}/recharge",
        json={"amount_cents": 2000},
        headers=headers,
    )
    assert recharge_response.status_code == 200
    assert recharge_response.json()["data"]["balance_cents"] == 12000

    freeze_response = test_client.post(
        f"/api/v1/member-cards/{card_id}/freeze",
        json={"frozen_from": "2026-05-10"},
        headers=headers,
    )
    assert freeze_response.status_code == 200
    assert freeze_response.json()["data"]["status"] == "frozen"

    unfreeze_response = test_client.post(
        f"/api/v1/member-cards/{card_id}/unfreeze", json={}, headers=headers
    )
    assert unfreeze_response.status_code == 200
    assert unfreeze_response.json()["data"]["status"] == "active"

    list_orders_response = test_client.get("/api/v1/orders", headers=headers)
    assert list_orders_response.status_code == 200
    assert list_orders_response.json()["data"]["total"] == 2

    list_cards_response = test_client.get(f"/api/v1/member-cards?member_id={member_id}", headers=headers)
    assert list_cards_response.status_code == 200
    assert list_cards_response.json()["data"]["total"] == 1

    get_card_response = test_client.get(f"/api/v1/member-cards/{card_id}", headers=headers)
    assert get_card_response.status_code == 200
    assert get_card_response.json()["data"]["id"] == card_id

    list_tx_response = test_client.get(f"/api/v1/member-cards/{card_id}/transactions", headers=headers)
    assert list_tx_response.status_code == 200
    assert list_tx_response.json()["data"]["total"] == 4

    first_order_id = list_orders_response.json()["data"]["items"][0]["id"]
    create_payment_response = test_client.post(
        "/api/v1/payments",
        json={"order_id": first_order_id, "method": "cash", "amount_cents": 500},
        headers=headers,
    )
    assert create_payment_response.status_code == 200
    assert create_payment_response.json()["data"]["order_id"] == first_order_id

    list_payments_response = test_client.get(f"/api/v1/payments?order_id={first_order_id}", headers=headers)
    assert list_payments_response.status_code == 200
    assert list_payments_response.json()["data"]["total"] == 1


def test_error_response_format(test_client):
    register_response = test_client.post(
        "/api/v1/auth/register",
        json={"username": "admin2", "password": "123456", "display_name": "Admin2"},
    )
    assert register_response.status_code == 200
    login_response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "admin2", "password": "123456"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    grant_response = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["transactions:write"]},
        headers=headers,
    )
    assert grant_response.status_code == 200

    response = test_client.post(
        "/api/v1/member-cards/open",
        json={"member_id": 9999, "card_type_id": 9999, "card_no": "C404"},
        headers=headers,
    )
    assert response.status_code == 404
    body = response.json()
    assert body["code"] == 40401
    assert body["message"] == "member not found"
    assert body["data"] is None


def test_transactions_requires_auth(test_client):
    response = test_client.get("/api/v1/orders")
    assert response.status_code == 401


def test_transactions_requires_permission(test_client):
    register_response = test_client.post(
        "/api/v1/auth/register",
        json={"username": "viewer", "password": "123456", "display_name": "Viewer"},
    )
    assert register_response.status_code == 200
    login_response = test_client.post(
        "/api/v1/auth/login",
        json={"username": "viewer", "password": "123456"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    denied_response = test_client.get("/api/v1/orders", headers=headers)
    assert denied_response.status_code == 403
    assert denied_response.json()["code"] == 40301
