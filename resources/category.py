from flask_jwt_extended import jwt_required, get_jwt
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.category import CategoryModel
from schemas import CategorySchema

blp = Blueprint("categories", __name__, description="Operations on categories")


@blp.route("/category/<string:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    @jwt_required()
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    def delete(self, category_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(403, message="Only admin can delete categories")
        category = CategoryModel.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()

        return {"message": "Category deleted."}, 200

    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    @jwt_required()
    def put(self, data, category_id):
        category = CategoryModel.query.get(category_id)
        if category:
            category.name = data["name"]
        else:
            category = CategoryModel(id=category_id, **data)

        db.session.add(category)
        db.session.commit()

        return category


@blp.route("/category")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    @jwt_required()
    def get(self):
        return CategoryModel.query.all()

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    @jwt_required()
    def post(self, data):
        category = CategoryModel(**data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Category already exists")
        except SQLAlchemyError:
            abort(500, message="Could not create category")

        return category
