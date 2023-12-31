#!/usr/bin/env python3
"""
auth.py module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Encrypts a password. Returns a salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initialize
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user in the database
        """
        try:
            registered_user = self._db.find_user_by(email=email)
            if registered_user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                        password.encode("utf-8"), user.hashed_password)
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Returns the session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Returns the corresponding User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Updates the corresponding user’s session ID to None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a UUID and update the user’s reset_token database field
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a users password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        updated_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=updated_password,
                             reset_token=None)
