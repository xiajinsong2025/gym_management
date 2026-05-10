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


def test_front_desk_flow(test_client):
    headers = _auth_headers(test_client, "front_admin_1")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["frontdesk:read", "frontdesk:write", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "FrontUser", "mobile": "13800000071", "member_no": "M7001"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    checkin = test_client.post(
        "/api/v1/checkins",
        json={"member_id": member_id, "bracelet_no": "B001"},
        headers=headers,
    )
    assert checkin.status_code == 200
    checkin_id = checkin.json()["data"]["id"]
    assert checkin.json()["data"]["status"] == "active"

    checkin_again = test_client.post(
        "/api/v1/checkins",
        json={"member_id": member_id},
        headers=headers,
    )
    assert checkin_again.status_code == 400
    assert checkin_again.json()["code"] == 40051

    checkout = test_client.post(f"/api/v1/checkins/{checkin_id}/checkout", json={}, headers=headers)
    assert checkout.status_code == 200
    assert checkout.json()["data"]["status"] == "checked_out"

    checkout_again = test_client.post(f"/api/v1/checkins/{checkin_id}/checkout", json={}, headers=headers)
    assert checkout_again.status_code == 400
    assert checkout_again.json()["code"] == 40052

    borrow = test_client.post(
        "/api/v1/bracelets/borrow",
        json={"member_id": member_id, "bracelet_no": "B001"},
        headers=headers,
    )
    assert borrow.status_code == 200
    assert borrow.json()["data"]["status"] == "borrowed"

    borrow_again = test_client.post(
        "/api/v1/bracelets/borrow",
        json={"member_id": member_id, "bracelet_no": "B001"},
        headers=headers,
    )
    assert borrow_again.status_code == 400
    assert borrow_again.json()["code"] == 40053

    returned = test_client.post("/api/v1/bracelets/B001/return", json={}, headers=headers)
    assert returned.status_code == 200
    assert returned.json()["data"]["status"] == "returned"

    returned_again = test_client.post("/api/v1/bracelets/B001/return", json={}, headers=headers)
    assert returned_again.status_code == 404
    assert returned_again.json()["code"] == 40452

    list_checkins = test_client.get("/api/v1/checkins?status=checked_out", headers=headers)
    assert list_checkins.status_code == 200
    assert list_checkins.json()["data"]["total"] >= 1

    list_bracelets = test_client.get("/api/v1/bracelets/records?bracelet_no=B001", headers=headers)
    assert list_bracelets.status_code == 200
    assert list_bracelets.json()["data"]["total"] == 1


def test_front_desk_requires_permission(test_client):
    headers = _auth_headers(test_client, "front_viewer")
    resp = test_client.get("/api/v1/checkins", headers=headers)
    assert resp.status_code == 403
    assert resp.json()["code"] == 40301
