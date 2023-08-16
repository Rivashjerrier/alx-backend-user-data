#!/usr/bin/env python3
"""
auth.py module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Encrypts a password. Returns a salted hash of the input password,
    hashed with bcrypt.hashpw
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
