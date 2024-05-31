from database import db

shopping_cart_products = db.Table(
    "shopping_cart_products",
    db.Column('shopping_cart_id', db.ForeignKey('shopping_carts.id'), primary_key=True),
    db.Column('product_id', db.ForeignKey('products.id'), primary_key=True),
    db.Column('quantity', db.Integer)
)