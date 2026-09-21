"""Password and database-backed session helpers; passwords are never stored in plain text."""
import base64
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import User, UserSession


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310_000)
    return f"pbkdf2_sha256$310000${base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, rounds, salt_text, digest_text = stored_hash.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), base64.b64decode(salt_text), int(rounds))
        return hmac.compare_digest(digest, base64.b64decode(digest_text))
    except (ValueError, TypeError):
        return False


def issue_session(db: Session, user: User) -> str:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expiry = datetime.now(UTC) + timedelta(hours=get_settings().session_expiry_hours)
    db.add(UserSession(user_id=user.id, token_hash=token_hash, expires_at=expiry))
    db.commit()
    return token


def get_user_for_token(db: Session, token: str) -> User | None:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    session = db.scalar(select(UserSession).where(UserSession.token_hash == token_hash))
    if not session or session.expires_at.replace(tzinfo=UTC) < datetime.now(UTC):
        return None
    return db.get(User, session.user_id)


def revoke_session(db: Session, token: str) -> None:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    session = db.scalar(select(UserSession).where(UserSession.token_hash == token_hash))
    if session:
        db.delete(session)
        db.commit()
