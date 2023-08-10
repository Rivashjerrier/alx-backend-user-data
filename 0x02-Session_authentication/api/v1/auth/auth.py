#!/usr/bin/env python3
"""
auth.py module
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Define which routes don't need authentication
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        paths = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if paths.startswith(excluded_path):
                    return False
            else:
                if paths == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Validates all requests to secure the API
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        session_cookie = request.cookies.get(_my_session_id, None)
        return session_cookie
