#!/usr/bin/env python3
''' Define the Auth class '''
from flask import request
from typing import List, TypeVar
import os
import re


class Auth:
    ''' Build Auth Object'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if the user is authenticated """
        if path is None or excluded_paths in [None, []]:
            return True
        for elem in excluded_paths:
            if elem[-1] == '*':
                save = '{}.*'.format(elem[0:-1])
            elif elem[-1] == '/':
                save = '{}/*'.format(elem[0:-1])
            else:
                save = '{}/*'.format(elem)
            if re.match(save, path):
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

    def session_cookie(self, request=None):
        """ Return a cookie value from a request
        """
        if request is None:
            return None
        cookie = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie)
