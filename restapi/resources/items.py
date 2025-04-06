
from flask_smorest import Blueprint, abort 
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel, StoreModel
from db import db 
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify
from custom_decorators import update_store, admin_required


blp = Blueprint("items", __name__, description="Operations on Items.")


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items
    

    #@jwt_required()    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        # store = StoreModel.query.get(item_data["store_id"])
        # if not store:
        #     abort(404, message="Store not Found.")

        try: 
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, 
                  message = "As error occured while inserting the item.")
            
        return item
    


@blp.route("/item/<int:item_id>")
class Items(MethodView):   
    @blp.response(200, ItemSchema)
    def get(self, item_id):                
        item = ItemModel.query.get_or_404(item_id)
        return item
    

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @update_store
    def put(self, item_data, item_id, store_updated=False):
        item = ItemModel.query.get_or_404(item_id)

        if not ( item.name == item_data["name"] and 
                item.price == item_data["price"] and store_updated == False):
            
            item.name = item_data["name"]
            item.price = item_data["price"]
    

            db.session.add(item)
            db.session.commit()

            item_data = ItemSchema().dump(item)

            return { "item": item_data , "message" : "Item updated."}, 200
        
        else:
             return {"message": "Nothing to update."}, 200        
       


    @jwt_required(fresh=True)
    @admin_required
    def delete(self, item_id):
        try: 
            item = ItemModel.query.get_or_404(item_id)
            
            db.session.delete(item)
            db.session.commit()
            return {"message" : "Item deleted"}, 200
        
        except StaleDataError as e:
            db.session.rollback()
            return {"message": "Stale data error: " + str(e)}, 409
       
        