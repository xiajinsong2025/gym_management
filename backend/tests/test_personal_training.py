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


def test_pt_flow(test_client):
    headers = _auth_headers(test_client, "pt_admin_1")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["pt:read", "pt:write", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "PTMember", "mobile": "13800000061", "member_no": "M6001"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    p1 = test_client.post(
        "/api/v1/pt/packages",
        json={
            "member_id": member_id,
            "name": "PT 10",
            "total_sessions": 10,
            "remaining_sessions": 10,
            "amount_cents": 200000,
        },
        headers=headers,
    )
    assert p1.status_code == 200
    package_id = p1.json()["data"]["id"]

    s1 = test_client.post(
        "/api/v1/pt/sessions",
        json={
            "package_id": package_id,
            "member_id": member_id,
            "coach_id": 1,
            "start_time": "2026-05-12T09:00:00Z",
            "end_time": "2026-05-12T10:00:00Z",
        },
        headers=headers,
    )
    assert s1.status_code == 200
    session_id = s1.json()["data"]["id"]
    assert s1.json()["data"]["status"] == "scheduled"

    c1 = test_client.post(f"/api/v1/pt/sessions/{session_id}/confirm", headers=headers)
    assert c1.status_code == 200
    assert c1.json()["data"]["status"] == "confirmed"

    consume = test_client.post(f"/api/v1/pt/sessions/{session_id}/consume", headers=headers)
    assert consume.status_code == 200
    assert consume.json()["data"]["status"] == "cancelled"

    list_packages = test_client.get(f"/api/v1/pt/packages?member_id={member_id}", headers=headers)
    assert list_packages.status_code == 200
    assert list_packages.json()["data"]["items"][0]["remaining_sessions"] == 9

    consume_again = test_client.post(f"/api/v1/pt/sessions/{session_id}/consume", headers=headers)
    assert consume_again.status_code == 400
    assert consume_again.json()["code"] == 40044


def test_pt_requires_permission(test_client):
    headers = _auth_headers(test_client, "pt_viewer")
    resp = test_client.get("/api/v1/pt/packages", headers=headers)
    assert resp.status_code == 403
    assert resp.json()["code"] == 40301
