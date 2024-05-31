from flask import Blueprint
from controllers.productController import create_product, find_all, get_product, update_product, delete_product

product_blueprint = Blueprint("product_bp", __name__)

product_blueprint.route('/', methods=['POST'])(create_product)
product_blueprint.route('/', methods=['GET'])(find_all) # view all products
product_blueprint.route('/<product_id>', methods=['GET'])(get_product) # view product at id
product_blueprint.route('/<product_id>', methods=['PUT'])(update_product) # update product at id
product_blueprint.route('/<product_id>', methods=['DELETE'])(delete_product) # delete product at id