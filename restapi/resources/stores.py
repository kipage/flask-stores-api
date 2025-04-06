from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema
from flask_jwt_extended import jwt_required
from custom_decorators import admin_required


blp = Blueprint("stores", __name__, description="Operation on Stores")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()

        return stores

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try: 
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,
                  message="A store with the name already exists.")
        except SQLAlchemyError:
            abort(500, 
                  message="An error occured while creating the store.")
            
        return store
        

        
@blp.route("/store/<int:store_id>")
class Stores(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
   
    
    @jwt_required(fresh=True)
    @admin_required
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted."}