def _auth_headers(test_client, username: str) -> dict[str, str]:
    register = test_client.post(
        "/api/v1/auth/register",
        json={"username": username, "password": "123456", "display_name": username},
    )
    assert register.status_code == 200
    login = test_client.post("/api/v1/auth/login", json={"username": username, "password": "123456"})
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_revenue_reports_flow(test_client):
    headers = _auth_headers(test_client, "report_admin_1")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={
            "codes": [
                "members:write",
                "transactions:read",
                "transactions:write",
                "reports:read",
            ]
        },
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "Reporter", "mobile": "13800000081", "member_no": "M8001"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    card_type = test_client.post(
        "/api/v1/card-types",
        json={"name": "Report Card", "kind": "stored_value", "price_cents": 10000},
        headers=headers,
    )
    assert card_type.status_code == 200
    card_type_id = card_type.json()["data"]["id"]

    open_card = test_client.post(
        "/api/v1/member-cards/open",
        json={
            "member_id": member_id,
            "card_type_id": card_type_id,
            "card_no": "R8001",
            "balance_cents": 10000,
            "total_amount_cents": 10000,
        },
        headers=headers,
    )
    assert open_card.status_code == 200

    orders = test_client.get("/api/v1/orders", headers=headers)
    assert orders.status_code == 200
    order_id = orders.json()["data"]["items"][0]["id"]

    payment = test_client.post(
        "/api/v1/payments",
        json={"order_id": order_id, "method": "cash", "amount_cents": 1000},
        headers=headers,
    )
    assert payment.status_code == 200

    daily = test_client.get("/api/v1/reports/revenue/daily", headers=headers)
    assert daily.status_code == 200
    assert len(daily.json()["data"]) >= 1
    assert daily.json()["data"][0]["order_paid_amount_cents"] >= 10000

    monthly = test_client.get("/api/v1/reports/revenue/monthly", headers=headers)
    assert monthly.status_code == 200
    assert len(monthly.json()["data"]) >= 1
    assert monthly.json()["data"][0]["payment_amount_cents"] >= 1000


def test_reports_requires_permission(test_client):
    headers = _auth_headers(test_client, "report_viewer")
    resp = test_client.get("/api/v1/reports/revenue/daily", headers=headers)
    assert resp.status_code == 403
    assert resp.json()["code"] == 40301
