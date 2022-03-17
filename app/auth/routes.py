from app import db, bcrypt
from app.auth import auth_bp
from flask import request, jsonify, session, make_response
from app.models.User import User


@auth_bp.route('/me')
def get_current_user():
    user_id = session.get('user_id')
    if user_id is None:
        return make_response({
            "error": "Unauthorized"
        }, 401)
    user = User.query.filter_by(id=user_id).first()
    return make_response({
        "userId": user.id,
        "email": user.email
    }, 200)


@auth_bp.route('/login', methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]
    # check if user exists
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "User does not exists!"}), 401
    # check if correct password
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Wrong password. Please try again!"}), 401
    # login user
    session.permanent = True
    session['user_id'] = user.id

    return make_response({
        "userId": user.id,
        "email": user.email,
    }, 200)


@auth_bp.route('/register', methods=["POST"])
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]
    # check if user is already registered
    user_exists = User.query.filter_by(email=email).first() is not None
    if user_exists:
        return jsonify({
            "error": "User already exists",
        }), 409
    # register new user
    hashed_password = bcrypt.generate_password_hash(password, 10)
    new_user = User(username=username,email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "userId": new_user.id,
        "email": new_user.email
    })


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({
        "message": "logged out"
    })


