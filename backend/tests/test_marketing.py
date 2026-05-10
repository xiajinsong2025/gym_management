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


def test_marketing_flow(test_client):
    headers = _auth_headers(test_client, "marketing_admin_1")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["marketing:read", "marketing:write", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "Lead1", "mobile": "13800000091", "member_no": "M9001"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    campaign = test_client.post(
        "/api/v1/marketing/campaigns",
        json={"title": "Summer Campaign", "status": "active"},
        headers=headers,
    )
    assert campaign.status_code == 200
    campaign_id = campaign.json()["data"]["id"]

    update_campaign = test_client.patch(
        f"/api/v1/marketing/campaigns/{campaign_id}",
        json={"content": "discount 20%"},
        headers=headers,
    )
    assert update_campaign.status_code == 200
    assert update_campaign.json()["data"]["content"] == "discount 20%"

    registration = test_client.post(
        f"/api/v1/marketing/campaigns/{campaign_id}/registrations",
        json={"member_id": member_id, "name": "Lead1", "mobile": "13800000091"},
        headers=headers,
    )
    assert registration.status_code == 200
    registration_id = registration.json()["data"]["id"]

    list_regs = test_client.get(f"/api/v1/marketing/campaigns/{campaign_id}/registrations", headers=headers)
    assert list_regs.status_code == 200
    assert list_regs.json()["data"]["total"] == 1

    update_reg = test_client.patch(
        f"/api/v1/marketing/registrations/{registration_id}",
        json={"note": "interested in PT"},
        headers=headers,
    )
    assert update_reg.status_code == 200
    assert update_reg.json()["data"]["note"] == "interested in PT"

    notice = test_client.post(
        "/api/v1/marketing/notifications",
        json={"title": "Holiday Notice", "content": "Closed on Sunday", "target_type": "all"},
        headers=headers,
    )
    assert notice.status_code == 200
    notice_id = notice.json()["data"]["id"]

    update_notice = test_client.patch(
        f"/api/v1/marketing/notifications/{notice_id}",
        json={"content": "Closed on Monday"},
        headers=headers,
    )
    assert update_notice.status_code == 200
    assert update_notice.json()["data"]["content"] == "Closed on Monday"

    list_notices = test_client.get("/api/v1/marketing/notifications", headers=headers)
    assert list_notices.status_code == 200
    assert list_notices.json()["data"]["total"] == 1


def test_marketing_requires_permission(test_client):
    headers = _auth_headers(test_client, "marketing_viewer")
    resp = test_client.get("/api/v1/marketing/campaigns", headers=headers)
    assert resp.status_code == 403
    assert resp.json()["code"] == 40301
