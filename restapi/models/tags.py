from db import db 

class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True )
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)  
    tag_description = db.Column(db.String(100))
    
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
