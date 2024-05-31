from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
from models.shoppingCartProducts import shopping_cart_products

class ShoppingCart(Base):
    __tablename__ = "shopping_carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
    customer: Mapped['Customer'] = db.relationship(back_populates='shopping_carts')
    
    # One-to-Many Relationship with Products, stored with quantity in shopping_cart_products table
    products: Mapped[List['Product']] = db.relationship(secondary=shopping_cart_products)