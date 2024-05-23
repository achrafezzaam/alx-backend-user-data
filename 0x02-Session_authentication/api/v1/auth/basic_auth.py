#!/usr/bin/env python3
''' Define the BasicAuth class '''
from .auth import Auth
import base64
from models.user import User
from typing import Tuple, TypeVar
import re


class BasicAuth(Auth):
    ''' Create the BasicAuth Object '''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Return the Base64 part of the Authorization header
        """
        if type(authorization_header) == str:
            token = r'Basic (?P<token>.+)'
            info_match = re.fullmatch(token, authorization_header.strip())
            if info_match is not None:
                return info_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """Decodes a base64-encoded authorization header.
        """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except Exception as e:
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Extracts user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.
        """
        if type(decoded_base64_authorization_header) == str:
            data = r'(?P<usr>[^:]+):(?P<pwd>.+)'
            info_match = re.fullmatch(
                data,
                decoded_base64_authorization_header.strip(),
            )
            if info_match is not None:
                usr = info_match.group('usr')
                pwd = info_match.group('pwd')
                return usr, pwd
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        header = self.authorization_header(request)
        auth_token = self.extract_base64_authorization_header(header)
        token = self.decode_base64_authorization_header(auth_token)
        mail, pwd = self.extract_user_credentials(token)
        return self.user_object_from_credentials(mail, pwd)
