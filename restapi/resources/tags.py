from flask.views import MethodView
from flask_smorest import Blueprint, abort 
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import TagSchema, TagAndItemSchema
from models import TagModel, ItemModel


blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id ):
        store = StoreModel.query.get_or_404(store_id)
        tags = store.tags.all()
        
        return tags
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id , TagModel.name == tag_data["name"]).first():
            abort(400, 
                message = "Tag with that name already exists."
            )

        tag = TagModel(**tag_data, store_id=store_id)

        try: 
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e : 
            abort(
                500,
                message=str(e)
            )
        
        return tag 

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItems(MethodView):
    @blp.response(200, TagAndItemSchema)
    def post(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        if tag in item.tags:
            return {"message": "Item already linked to tag."}
              
        try: 
            item.tags.append(tag)
            db.session.add(item)    
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occured while linking the tag to the item.")
        
        return {"message": "Item linked to the tag.", "item": item, "tag": tag }
    
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        #item.tags.remove(tag)
        if tag.items: 
            item.tags.remove(tag)
        
            try:            
                #db.session.add(item)
                db.session.add(tag) 
                db.session.commit()
            except SQLAlchemyError:
                abort(500,
                    message="An error occured while unlinking the tag from the item.")
        
            return {"message": "Item removed from tag.", "item": item, "tag": tag }
        
        else:
            return {"message": "Item not linked to tag."}



@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(
        200, 
        description="Delete a tag if no item is tagged with it",
         example={ "messsage": "Tag deleted."} )
    @blp.alt_response(
        400, 
        description="Tag is linked to an item.")
    @blp.alt_response(
            404,
            description="Tag not found.")
    @blp.alt_response(
        500, 
        description="An error occured while deleting the tag.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        
        if tag.items:
            abort(400,
                  message="Tag is linked to an item.")
        
        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occured while deleting the tag.")
        
        return {"message": "Tag deleted."}