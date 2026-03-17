"""
Authentication Module for KadiRail AI
Simple session-based authentication
"""

import hashlib
import secrets
import time
from typing import Optional, Dict
from dataclasses import dataclass, field


@dataclass
class User:
    username: str
    password_hash: str
    role: str = "user"
    created_at: float = field(default_factory=time.time)


class AuthManager:
    """
    Simple authentication manager for KadiRail AI

    For production, replace with proper OAuth/AAA integration
    """

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Dict] = {}
        self._init_default_users()

    def _init_default_users(self):
        """Initialize default users (demo)"""
        default_users = [
            ("admin", "kadirail2026", "admin"),
            ("demo", "demo1234", "user"),
            ("reviewer", "review2026", "reviewer"),
        ]

        for username, password, role in default_users:
            self.users[username] = User(
                username=username,
                password_hash=self._hash_password(password),
                role=role,
            )

    def _hash_password(self, password: str, salt: str = "kadirail_salt") -> str:
        """Hash password with salt"""
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

    def _generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)

    def login(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user and create session

        Returns:
            dict with session info or None if failed
        """
        user = self.users.get(username)

        if not user:
            return None

        if user.password_hash != self._hash_password(password):
            return None

        # Create session
        token = self._generate_session_token()
        self.sessions[token] = {
            "username": username,
            "role": user.role,
            "login_time": time.time(),
            "expires_at": time.time() + (24 * 3600),  # 24 hours
        }

        return {"token": token, "username": username, "role": user.role}

    def logout(self, token: str) -> bool:
        """Invalidate session"""
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False

    def verify_session(self, token: str) -> Optional[Dict]:
        """Verify session is valid"""
        session = self.sessions.get(token)

        if not session:
            return None

        # Check expiration
        if time.time() > session["expires_at"]:
            self.logout(token)
            return None

        return session

    def change_password(
        self, username: str, old_password: str, new_password: str
    ) -> bool:
        """Change user password"""
        user = self.users.get(username)

        if not user:
            return False

        if user.password_hash != self._hash_password(old_password):
            return False

        user.password_hash = self._hash_password(new_password)
        return True

    def add_user(self, username: str, password: str, role: str = "user") -> bool:
        """Add new user"""
        if username in self.users:
            return False

        self.users[username] = User(
            username=username, password_hash=self._hash_password(password), role=role
        )
        return True


# Global auth manager instance
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get or create auth manager singleton"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


def require_auth(func):
    """Decorator to require authentication"""

    def wrapper(*args, **kwargs):
        import streamlit as st

        # Check session
        if "auth_token" not in st.session_state:
            st.error("กรุณาเข้าสู่ระบบก่อน")
            st.stop()

        auth = get_auth_manager()
        session = auth.verify_session(st.session_state.auth_token)

        if not session:
            st.error("Session หมดอายุ กรุณาเข้าสู่ระบบใหม่")
            if "auth_token" in st.session_state:
                del st.session_state.auth_token
            st.stop()

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def require_role(*allowed_roles):
    """Decorator to require specific role"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            import streamlit as st

            if "session" not in st.session_state:
                st.error("กรุณาเข้าสู่ระบบก่อน")
                st.stop()

            user_role = st.session_state.session.get("role")

            if user_role not in allowed_roles:
                st.error(f"ไม่มีสิทธิ์เข้าถึง (ต้องการ: {', '.join(allowed_roles)})")
                st.stop()

            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return decorator
