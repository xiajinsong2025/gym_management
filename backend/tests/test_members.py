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


def test_member_detail_update_and_search(test_client):
    headers = _auth_headers(test_client, "member_admin_1")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["members:read", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    first = test_client.post(
        "/api/v1/members",
        json={"name": "Alice", "mobile": "13800000011", "member_no": "M2001"},
        headers=headers,
    )
    assert first.status_code == 200
    first_id = first.json()["data"]["id"]

    second = test_client.post(
        "/api/v1/members",
        json={"name": "Bob", "mobile": "13800000012", "member_no": "M2002"},
        headers=headers,
    )
    assert second.status_code == 200

    detail = test_client.get(f"/api/v1/members/{first_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["name"] == "Alice"

    update = test_client.patch(
        f"/api/v1/members/{first_id}",
        json={"status": "frozen", "remark": "manual freeze"},
        headers=headers,
    )
    assert update.status_code == 200
    assert update.json()["data"]["status"] == "frozen"
    assert update.json()["data"]["remark"] == "manual freeze"

    by_keyword = test_client.get("/api/v1/members?keyword=Bob", headers=headers)
    assert by_keyword.status_code == 200
    assert by_keyword.json()["data"]["total"] == 1
    assert by_keyword.json()["data"]["items"][0]["name"] == "Bob"

    by_status = test_client.get("/api/v1/members?status=frozen", headers=headers)
    assert by_status.status_code == 200
    assert by_status.json()["data"]["total"] == 1
    assert by_status.json()["data"]["items"][0]["id"] == first_id


def test_member_not_found(test_client):
    headers = _auth_headers(test_client, "member_admin_2")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["members:read", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    detail = test_client.get("/api/v1/members/9999", headers=headers)
    assert detail.status_code == 404
    assert detail.json()["code"] == 40401

    update = test_client.patch("/api/v1/members/9999", json={"name": "Nobody"}, headers=headers)
    assert update.status_code == 404
    assert update.json()["code"] == 40401


def test_member_profile_upsert_and_get(test_client):
    headers = _auth_headers(test_client, "member_admin_3")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["members:read", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "Carol", "mobile": "13800000021", "member_no": "M3001"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    upsert = test_client.put(
        f"/api/v1/members/{member_id}/profile",
        json={"height_cm": 170, "weight_kg": 65, "fitness_goal": "fat loss"},
        headers=headers,
    )
    assert upsert.status_code == 200
    assert upsert.json()["data"]["height_cm"] == 170

    get_profile = test_client.get(f"/api/v1/members/{member_id}/profile", headers=headers)
    assert get_profile.status_code == 200
    assert get_profile.json()["data"]["fitness_goal"] == "fat loss"


def test_member_followups_crud_like_flow(test_client):
    headers = _auth_headers(test_client, "member_admin_4")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["members:read", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "David", "mobile": "13800000022", "member_no": "M3002"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    created = test_client.post(
        f"/api/v1/members/{member_id}/followups",
        json={"content": "first call", "next_followup_date": "2026-05-20"},
        headers=headers,
    )
    assert created.status_code == 200
    followup_id = created.json()["data"]["id"]

    listed = test_client.get(f"/api/v1/members/{member_id}/followups", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1
    assert listed.json()["data"]["items"][0]["id"] == followup_id

    updated = test_client.patch(
        f"/api/v1/members/{member_id}/followups/{followup_id}",
        json={"content": "second call"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["content"] == "second call"


def test_member_feedback_flow(test_client):
    headers = _auth_headers(test_client, "member_admin_5")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["members:read", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "Eve", "mobile": "13800000031", "member_no": "M4001"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    created = test_client.post(
        f"/api/v1/members/{member_id}/feedback",
        json={"category": "service", "content": "too crowded"},
        headers=headers,
    )
    assert created.status_code == 200
    feedback_id = created.json()["data"]["id"]
    assert created.json()["data"]["status"] == "open"

    listed = test_client.get(f"/api/v1/members/{member_id}/feedback", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1

    updated = test_client.patch(
        f"/api/v1/members/{member_id}/feedback/{feedback_id}",
        json={"status": "closed", "reply": "optimized schedule"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["status"] == "closed"


def test_training_records_flow(test_client):
    headers = _auth_headers(test_client, "member_admin_6")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["members:read", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "Frank", "mobile": "13800000032", "member_no": "M4002"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    created = test_client.post(
        f"/api/v1/members/{member_id}/training-records",
        json={"record_date": "2026-05-10", "content": "bench press 60kg"},
        headers=headers,
    )
    assert created.status_code == 200
    record_id = created.json()["data"]["id"]

    listed = test_client.get(f"/api/v1/members/{member_id}/training-records", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1

    updated = test_client.patch(
        f"/api/v1/members/{member_id}/training-records/{record_id}",
        json={"content": "bench press 65kg"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["content"] == "bench press 65kg"


def test_members_requires_permission(test_client):
    headers = _auth_headers(test_client, "member_viewer")
    response = test_client.get("/api/v1/members", headers=headers)
    assert response.status_code == 403
    assert response.json()["code"] == 40301
