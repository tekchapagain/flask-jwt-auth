from datetime import datetime, timezone
from server import db
from typing import List
from sqlalchemy import func


class ProductModel(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    stock_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    category = db.relationship('CategoryModel',back_populates='products')

    def __init__(self, name, price,description, stock_quantity,category_id):
        self.name = name
        self.price = price
        self.description = description
        self.stock_quantity = stock_quantity
        self.category_id = category_id

    def __repr__(self):
        return 'ProductModel(name=%s,price=%s,description=%s,stock_quantity=%s)' % (self.name,self.price,self.description,self.stock_quantity)

    def json(self):
        return {
                 'id' : self.id,
                 'name': self.name,
                 'price': self.price,
                 'description': self.description,
                 'stock_quantity':self.stock_quantity,
                 'category_id':self.category_id
               }

    @classmethod
    def find_by_name(cls, name) -> "ProductModel":
        return cls.query.filter(func.lower(cls.name) == func.lower(name)).first()

    @classmethod
    def find_by_id(cls, _id) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ProductModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
