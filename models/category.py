from server import db
from sqlalchemy import func
from typing import List


class CategoryModel(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    category_name = db.Column(db.String(80), nullable=False, unique=True)
    products = db.relationship("ProductModel", lazy="dynamic", primaryjoin="CategoryModel.category_id == ProductModel.category_id")
    def __init__(self, name):
        self.category_name = name

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return 'CategoryModel(category_name=%s)' % (self.category_name)

    def json(self):
        return {
            'category_id' : self.category_id,
            'category_name': self.category_name,
            'products': [product.json() for product in self.products.all()]
            }

    @classmethod
    def find_by_category_name(cls, category_name) -> "CategoryModel":
        return cls.query.filter(func.lower(cls.category_name) == func.lower(category_name)).first()

    @classmethod
    def find_by_id(cls, _id) -> "CategoryModel":
        return cls.query.filter_by(category_id=_id).first()

    @classmethod
    def find_all(cls) -> List["CategoryModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
