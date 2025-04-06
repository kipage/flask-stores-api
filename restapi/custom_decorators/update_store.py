from functools import wraps
from models import ItemModel, StoreModel
from schemas import ItemSchema
from flask_smorest import abort
from db import db


def update_store(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        item_data, item_id, = dict(args[1]), kwargs

        item = ItemModel.query.get(item_id['item_id']) 
        if not item:
             abort(404, message="Item not available to update.")

        store = StoreModel.query.get(item_data["store_id"])
        if not store:
            abort(404, message="Store not available to update.")

        if not item.store or  item.store.id != item_data["store_id"]:
            item.store_id = item_data["store_id"]
            db.session.add(item)
            db.session.commit()

            return func(*args, **kwargs, store_updated=True)
        
        else : 

            return func(*args, **kwargs)
        
    return wrapper