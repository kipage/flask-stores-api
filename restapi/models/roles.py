from db import db 

class RoleModel(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship("UserModel", back_populates="roles", secondary="users_roles")