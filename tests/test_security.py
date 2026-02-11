from fastapi.testclient import TestClient


def test_admin_requires_login():
    from app.main import app

    client = TestClient(app)
    resp = client.get("/admin", follow_redirects=False)
    assert resp.status_code in (302, 307)
    assert "/auth/login" in resp.headers.get("location", "")


def test_post_requires_csrf_on_login():
    from app.main import app

    import re

    client = TestClient(app)
    # POST to login without csrf_token -> FastAPI validation fails (missing form field)
    resp = client.post("/auth/login", data={"username": "x", "password": "y"}, follow_redirects=False)
    assert resp.status_code == 422

    # Get the login page to obtain a valid csrf token stored in session
    rpage = client.get("/auth/login")
    assert rpage.status_code == 200
    m = re.search(r'name="csrf_token" value="([^"]+)"', rpage.text)
    assert m, "csrf_token input not found in login page"
    valid_token = m.group(1)

    # Wrong token should be rejected with 400
    resp_bad = client.post(
        "/auth/login",
        data={"username": "x", "password": "y", "csrf_token": "bad-token"},
        follow_redirects=False,
    )
    assert resp_bad.status_code == 400
