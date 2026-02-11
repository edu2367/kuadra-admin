import os
import re
import time
import uuid
import pytest


pytestmark = pytest.mark.usefixtures


def test_redis_session_flow():
    # Skip if not running with REDIS_URL (CI will set this)
    REDIS_URL = os.getenv("REDIS_URL")
    if not REDIS_URL:
        pytest.skip("REDIS_URL not set; skipping Redis session test")

    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # register a unique user
    uniq = str(uuid.uuid4())[:8]
    email = f"test+{uniq}@example.com"
    pw = "secret123"

    # get register page and extract csrf
    r = client.get("/auth/register")
    assert r.status_code == 200
    m = re.search(r'name="csrf_token" value="([^"]+)"', r.text)
    assert m
    token = m.group(1)

    resp = client.post(
        "/auth/register",
        data={
            "first_name": "T",
            "last_name": "User",
            "email": email,
            "password": pw,
            "password2": pw,
            "csrf_token": token,
        },
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)

    # login with that user
    r2 = client.get("/auth/login")
    assert r2.status_code == 200
    m2 = re.search(r'name="csrf_token" value="([^"]+)"', r2.text)
    assert m2
    token2 = m2.group(1)

    resp2 = client.post(
        "/auth/login",
        data={"username": email, "password": pw, "csrf_token": token2},
        follow_redirects=False,
    )
    assert resp2.status_code in (302, 303)

    # now accessing admin/dashboard should be allowed (200)
    r3 = client.get("/admin/dashboard")
    assert r3.status_code == 200
