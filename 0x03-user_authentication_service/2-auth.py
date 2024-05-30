#!/usr/bin/env python3
""" Handles the authentication process """
from db import DB
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """Return the bytes formated hashed password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """Generate a uuid
    """
    from uuid import uuid4
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new User
        """
        try:
            self._db.find_user_by(email=email)
        except Exception as e:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the given password match the user's hash password
        """
        import bcrypt
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return False
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """Generate a new UUID and store it in the database as
            the user’s session_id
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return user.session_id
