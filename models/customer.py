from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    username: Mapped[str] = mapped_column(db.String(100), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    # One-to-Many Relationship with Orders
    orders: Mapped[List['Order']] = db.relationship(back_populates='customer')
    shopping_carts: Mapped[List['ShoppingCart']] = db.relationship(back_populates='customer')

    def __repr__(self):
        return f"<Customer {self.id}|{self.name}>"