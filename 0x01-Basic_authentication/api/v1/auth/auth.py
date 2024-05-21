#!/usr/bin/env python3
''' Define the Auth class '''
from flask import request
from typing import List, TypeVar


class Auth:
    ''' Build Auth Object'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if the user is authenticated """
        if path is None or excluded_paths in [None, []]:
            return True
        if path in excluded_paths or (path + '/') in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Build the authorization header
        """
        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return the current user
        """
        return None
