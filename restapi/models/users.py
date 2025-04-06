from db import db


class UserModel(db.Model): 
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable = False )
    email = db.Column(db.String(80), unique=True, nullable=False)

    #role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    roles = db.relationship("RoleModel", back_populates="users", secondary="users_roles")

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "username": self.username,
    #         "password": self.password,
    #         "roles": [role.role for role in self.roles]
    #     }