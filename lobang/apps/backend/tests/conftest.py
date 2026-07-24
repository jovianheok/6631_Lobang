"""
Shared fixtures for the backend test suite.

The app is imported once here with dummy env vars so importing it never needs a
real Supabase project or database. Route tests override the auth dependencies
(so no real JWT is required) and patch the service layer (so no real DB is hit).
"""

import os

# Must be set BEFORE importing the app: src.auth.supabase_auth reads SUPABASE_URL
# at import time to build its JWKS client (the client is lazy, so a dummy URL is
# fine). connection.py only reads DATABASE_URL when get_conn() is called.
os.environ.setdefault("SUPABASE_URL", "https://dummy.supabase.co")
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/dummy")

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.auth.supabase_auth import get_current_user, get_optional_current_user


@pytest.fixture
def client():
    """A TestClient with auth overrides cleared after each test."""
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def as_user():
    """Override auth so requests are treated as a signed-in user."""
    def _login(user_id: str = "user-123") -> str:
        app.dependency_overrides[get_current_user] = lambda: user_id
        app.dependency_overrides[get_optional_current_user] = lambda: user_id
        return user_id

    return _login


@pytest.fixture
def as_guest():
    """Override optional auth so requests are treated as anonymous."""
    def _guest() -> None:
        app.dependency_overrides[get_optional_current_user] = lambda: None

    return _guest
