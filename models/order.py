from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from typing import List
from models.orderProducts import order_products

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Many-to-One Relationship with Customers
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
    customer: Mapped['Customer'] = db.relationship(back_populates='orders')
    
    # One-to-Many Relationship with Products, stored with quantity in order_products table
    products: Mapped[List['Product']] = db.relationship(secondary=order_products)
    
    # not set in schema, but in system logic
    order_date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=lambda : datetime.datetime.date(datetime.datetime.now()))
    delivery_date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    total_price: Mapped[float] = mapped_column(db.Float, nullable=False)
    cancelled: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)


    # TO-DO: BONUSES:
        # Manage Order History (Bonus): Create an endpoint that allows customers to access their order history, listing all previous orders placed. Each order entry should provide comprehensive information, including the order date and associated products.
        # Cancel Order (Bonus): Implement an order cancellation feature, allowing customers to cancel an order if it hasn't been shipped or completed. Ensure that canceled orders are appropriately reflected in the system.
        # Calculate Order Total Price (Bonus): Include an endpoint that calculates the total price of items in a specific order, considering the prices of the products included in the order. This calculation should be specific to each customer and each order, providing accurate pricing information.