from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainRoleSchema, RoleSchema
from models import RoleModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError




blp = Blueprint("roles", __name__, description="Operations on roles")

@blp.route("/role")
class RoleList(MethodView):
    @blp.response(200, PlainRoleSchema(many=True))
    def get(self):
        roles = RoleModel.query.all()

        return roles

    @blp.arguments(RoleSchema)
    @blp.response(201, PlainRoleSchema)
    def post(self, role_data):
        role = RoleModel(**role_data)
        try: 
            db.session.add(role)
            db.session.commit()
        except IntegrityError:
            abort(400,
                  message="A role with the name already exists.")
        except SQLAlchemyError:
            abort(500, 
                  message="An error occured while creating the role.")
            
        return role

@blp.route("/role/<int:role_id>")
class Roles(MethodView):
    @blp.response(200, RoleSchema)
    def get(self, role_id):
        role = RoleModel.query.get_or_404(role_id)
        return role

    def delete(self, role_id):
        role = RoleModel.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()

        return {"message": "Role deleted."}
    
