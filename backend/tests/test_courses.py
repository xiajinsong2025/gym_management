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


def test_courses_flow(test_client):
    headers = _auth_headers(test_client, "course_admin_1")
    grant = test_client.post(
        "/api/v1/auth/me/permissions",
        json={"codes": ["courses:read", "courses:write", "members:write"]},
        headers=headers,
    )
    assert grant.status_code == 200

    member = test_client.post(
        "/api/v1/members",
        json={"name": "Booker", "mobile": "13800000051", "member_no": "M5001"},
        headers=headers,
    )
    assert member.status_code == 200
    member_id = member.json()["data"]["id"]

    c1 = test_client.post("/api/v1/course-categories", json={"name": "Yoga"}, headers=headers)
    assert c1.status_code == 200
    category_id = c1.json()["data"]["id"]

    c2 = test_client.post(
        "/api/v1/courses",
        json={"category_id": category_id, "name": "Morning Yoga", "default_capacity": 10, "duration_minutes": 60},
        headers=headers,
    )
    assert c2.status_code == 200
    course_id = c2.json()["data"]["id"]

    s1 = test_client.post(
        "/api/v1/course-schedules",
        json={
            "course_id": course_id,
            "start_time": "2026-05-11T09:00:00Z",
            "end_time": "2026-05-11T10:00:00Z",
            "capacity": 1,
        },
        headers=headers,
    )
    assert s1.status_code == 200
    schedule_id = s1.json()["data"]["id"]

    b1 = test_client.post(
        f"/api/v1/course-schedules/{schedule_id}/bookings",
        json={"member_id": member_id},
        headers=headers,
    )
    assert b1.status_code == 200
    assert b1.json()["data"]["status"] == "booked"

    m2 = test_client.post(
        "/api/v1/members",
        json={"name": "Waiter", "mobile": "13800000052", "member_no": "M5002"},
        headers=headers,
    )
    assert m2.status_code == 200
    member2_id = m2.json()["data"]["id"]
    b2 = test_client.post(
        f"/api/v1/course-schedules/{schedule_id}/bookings",
        json={"member_id": member2_id},
        headers=headers,
    )
    assert b2.status_code == 200
    assert b2.json()["data"]["status"] == "waitlisted"
    booking2_id = b2.json()["data"]["id"]

    l1 = test_client.get(f"/api/v1/course-schedules/{schedule_id}/bookings", headers=headers)
    assert l1.status_code == 200
    assert l1.json()["data"]["total"] == 2

    u1 = test_client.patch(f"/api/v1/course-bookings/{booking2_id}", json={"status": "cancelled"}, headers=headers)
    assert u1.status_code == 200
    assert u1.json()["data"]["status"] == "cancelled"

    ls = test_client.get(f"/api/v1/course-schedules?course_id={course_id}", headers=headers)
    assert ls.status_code == 200
    data = ls.json()["data"]["items"][0]
    assert data["booked_count"] == 1
    assert data["waitlisted_count"] == 0


def test_courses_requires_permission(test_client):
    headers = _auth_headers(test_client, "course_viewer")
    resp = test_client.get("/api/v1/courses", headers=headers)
    assert resp.status_code == 403
    assert resp.json()["code"] == 40301
