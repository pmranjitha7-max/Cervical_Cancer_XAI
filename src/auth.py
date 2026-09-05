"""
Small, dependency-free password hashing + auth helpers (PBKDF2-HMAC-SHA256
via Python's standard library, so we don't need to add bcrypt/passlib to
requirements.txt just for this).
"""
from __future__ import annotations

import hashlib
import hmac
import re
import secrets

from fastapi import Header, HTTPException

from . import db

PBKDF2_ITERATIONS = 200_000
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ITERATIONS
    )
    return derived.hex(), salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    candidate, _ = hash_password(password, salt)
    return hmac.compare_digest(candidate, password_hash)


def validate_registration(name: str, username: str, email: str, password: str):
    if len(name.strip()) < 2:
        raise HTTPException(400, "Please enter your full name.")
    if len(username.strip()) < 4:
        raise HTTPException(400, "Username must be at least 4 characters.")
    if not EMAIL_RE.match(email.strip()):
        raise HTTPException(400, "Please enter a valid email address.")
    if len(password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters.")


def get_current_user(authorization: str | None = Header(default=None)):
    """Required auth dependency — raises 401 if there is no valid session."""
    user = get_optional_user(authorization)
    if user is None:
        raise HTTPException(status_code=401, detail="Sign in required.")
    return user


def get_optional_user(authorization: str | None = Header(default=None)):
    """Optional auth dependency — returns None instead of raising, so
    endpoints like /cancer-report keep working without a login but will
    save history automatically when a valid token is presented."""
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    user_id = db.get_user_id_for_token(token)
    if user_id is None:
        return None
    return db.get_user_by_id(user_id)
