# James Carlson
# Coding Temple - SE FT-144
# Backend Specialization, Module 13 Lesson 1 Assignment: REST API Design Patterns

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from database import db
from schemas import ma
from limiter import limiter
from caching import cache

from models.customer import Customer
from models.product import Product
from models.order import Order
from models.orderProducts import order_products
from models.shoppingCart import ShoppingCart
from models.shoppingCartProducts import shopping_cart_products

from routes.customerBP import customer_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.shoppingCartBP import shopping_cart_blueprint
from routes.loginBP import login_blueprint


SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI
API_URL = '/static/swagger.yaml' # Pth to the YAML file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'CT E-Commerce API'}
)

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    migrate = Migrate(app, db)

    blueprint_config(app)
    config_rate_limit()
    
    return app

def blueprint_config(app):
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(shopping_cart_blueprint, url_prefix='/cart')
    app.register_blueprint(login_blueprint, url_prefix='/login')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def config_rate_limit():
    limiter.limit("100 per day")(customer_blueprint)
    limiter.limit("100 per day")(product_blueprint)
    limiter.limit("100 per day")(order_blueprint)
    limiter.limit("100 per day")(shopping_cart_blueprint)

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
        
    app.run(debug=True)