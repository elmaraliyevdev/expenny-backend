import uuid
from flask import request
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.user import UserModel
from schemas import UserSchema
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        user = UserModel(username=data["username"], password=sha256.hash(data["password"]), email=data["email"])
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="User already exists")
        except SQLAlchemyError:
            abort(500, message="Could not create user")

        return {"message": "User created successfully."}, 201


@blp.route("/user/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, data):
        user = UserModel.query.filter(UserModel.email == data["email"]).first()
        if user and sha256.verify(data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials")


@blp.route("/user/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@blp.route("/user/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out successfully."}, 200


@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted."}, 200

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, data, user_id):
        user = UserModel.query.get(user_id)
        if user:
            user.username = data["username"]
            user.email = data["email"]
            user.password = data["password"]
        else:
            user = UserModel(id=user_id, **data)

        db.session.add(user)
        db.session.commit()

        return user
