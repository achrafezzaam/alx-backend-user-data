#!/usr/bin/env python3
''' Session authentication views '''
import os
from typing import Tuple
from flask import request, jsonify
from models.user import User
from api.v1.views import app_views


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False
        )
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    """
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    pwd = request.form.get('password')
    if pwd is None or pwd == '':
        return jsonify({"error": "password missing"}), 400
    try:
        user = User.search({'email': email})
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user) < 1:
        return jsonify({"error": "no user found for this email"}), 404
    if user[0].is_valid_password(pwd):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(user[0], 'id'))
        res = jsonify(user[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
        )
def logout():
    """DELETE /api/v1/auth_session/logout
    Return:
      - Empty JSON.
    """
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if not destroyed:
        abort(404)
    return jsonify({}), 200
