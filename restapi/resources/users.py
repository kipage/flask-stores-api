from models import UserModel, BlackListModel, RoleModel
from sqlalchemy import or_
from flask.views import MethodView
from flask_smorest import Blueprint,  abort
from db import db 
from datetime import datetime
from schemas import PlainUserSchema, UserSchema, BlacklistSchema, UserRegisterSchema, UserRegisterSchema
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity


blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    #@blp.response(201, UserRegisterSchema)
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
            UserModel.username==user_data["username"],
            UserModel.email==user_data["email"] 
                )
            ).first():
            abort(400, message="User with that username or email ID already exists.")
       
        roles = RoleModel.query.filter(RoleModel.role == 'user').first()
        role = [roles]

        user = UserModel(
            username=user_data["username"],
            password=sha256.hash(user_data["password"]),
            email = user_data["email"],
            roles = role
        ) 

        db.session.add(user)
        db.session.commit()
        
        return { "message": "User created successfully." }, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data["username"]).first()
              
        if user and sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return { "access_token": access_token , "refresh_token": refresh_token}, 200
        
        abort(401, message="Invalid credentials.")



def blacklist():
    blacklist = BlackListModel(
        token = get_jwt()["jti"],
        blacklisted_on = datetime.now()
    )
    db.session.add(blacklist)
    db.session.commit()
    return { "message": "Token blacklisted." }, 200
    

@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        token = get_jwt()["jti"]
        if not token:
            abort(400, message="Token is missing.")

        blacklist()
        return { "message": "User logged out successfully." }, 200
    

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_refresh_token(identity=current_user)
        jti = get_jwt()["jti"]
        blacklist()   
        return { "refresh_token": access_token }, 200


@blp.route("/users")
class Users(MethodView):
    @blp.response(200, UserRegisterSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users



@blp.route("/user/<int:user_id>")
class UserList(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 201
    
    
@blp.route("/user/<int:user_id>/role/<int:role_id>")
class AssignRole(MethodView):
    @blp.response(200, UserSchema)
    def post(self, user_id, role_id):
        user = UserModel.query.get_or_404(user_id)
        role = RoleModel.query.get_or_404(role_id)

        if role in user.roles:
            abort(400, message="User already has that role.")

        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        return user