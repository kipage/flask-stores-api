import os  
import datetime
from flask import Flask, jsonify
from flask_smorest import Api
from resources.items import blp as ItemBluprint
from resources.stores import blp as StoreBluprint
from resources.tags import blp as TagBluprint
from resources.users import blp as UserBluprint
from resources.roles import blp as RoleBluprint
import models 
from db import db 
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from defaults import create_default_roles



def create_app(db_url=None):

    app = Flask(__name__)
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "Super_secret"

    # jwt_expire = datetime.timedelta(minutes=30)
    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_expire 
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=1)

    db.init_app(app)               # conecting the database to the app
    migrate = Migrate(app, db)     # connecting the migration to the app and the database
    api = Api(app)                 # connecting the api to the app
    jwt = JWTManager(app)          # connecting the jwt extension to the app


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        if not models.BlackListModel.query.filter_by(token=jti).first():
            return False
        return True

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user = models.UserModel.query.get(identity)
        roles = [role.role for role in user.roles]
        
        username = models.UserModel.query.get(identity).username

        return {"role": roles , "username": username}


    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "Token is not fresh.", "error": "Fresh token required."}), 401)
    

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has been expired.",  "error": "Token expired."}), 
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed.", "error": "Invalid token."}),
            401,
        )   
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {"message": "Request does not contain an access token.", "error" : "Token missing."}
            ),
              401,
        )

    # @app.before_request
    # def create_tables():
    #     db.create_all()

    #create default roles
    
    with app.app_context():
        create_default_roles()
    

    api.register_blueprint(ItemBluprint)
    api.register_blueprint(StoreBluprint)
    api.register_blueprint(TagBluprint)
    api.register_blueprint(UserBluprint)
    api.register_blueprint(RoleBluprint)
    


    return app

