
from db import db
from models import RoleModel


def create_default_roles():

    default_user_role = RoleModel.query.filter(RoleModel.role =='user').first()
    if default_user_role is None:
        default_user_role = RoleModel(role='user')
        db.session.add(default_user_role)
        db.session.commit()
    
    admin_role = RoleModel.query.filter(RoleModel.role =='admin').first()
    if not admin_role:
        admin_role = RoleModel(role='admin')
        db.session.add(admin_role)
        db.session.commit()


