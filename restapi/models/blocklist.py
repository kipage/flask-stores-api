from db import db 


class BlackListModel(db.Model):
    __tablename__ = "blocklist"

    id = db.Column(db.Integer, primary_key=True)    
    token = db.Column(db.String(80), nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)