#!/usr/bin/env python3
''' Define the app routes '''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /
        Return: The payload {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
        Return: The account creation payload
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
            })
    except Exception as e:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
        Return: The account creation payload
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    cookie = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", cookie)
    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> None:
    """DELETE /sessions
    """
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> None:
    """GET /profile
        Return: The profile payload
    """
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> None:
    """POST /reset_password
    """
    email = request.form.get("email")
    try:
        user = AUTH.get_reset_password_token(email)
    except Exception as e:
        abort(403)
    return jsonify({
        "email": email,
        "reset_token": user.reset_token
        }), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> None:
    """PUT /reset_password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception as e:
        abort(403)
    return jsonify({
        "email": email,
        "message": "Password updated"
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
