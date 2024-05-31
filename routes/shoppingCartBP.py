from flask import Blueprint
from controllers.shoppingCartController import create_cart, find_all, get_shopping_cart, add_to_cart, remove_from_cart, update_item_qty, empty_cart, checkout, set_active_cart

shopping_cart_blueprint = Blueprint("shopping_cart_bp", __name__)

# create empty cart
shopping_cart_blueprint.route('/', methods=['POST'])(create_cart) 

# view shopping cart at id
shopping_cart_blueprint.route('/<shopping_cart_id>', methods=['GET'])(get_shopping_cart) 

# view all shopping carts
shopping_cart_blueprint.route('/', methods=['GET'])(find_all) 

# add product to cart
shopping_cart_blueprint.route('/add/<product_id>', methods=['PUT'])(add_to_cart) 

# remove product from cart
shopping_cart_blueprint.route('/remove/<product_id>', methods=['PUT'])(remove_from_cart) 

# update product quantity (with json body)
shopping_cart_blueprint.route('/update/<product_id>', methods=['PUT'])(update_item_qty) 

# empty cart of all products
shopping_cart_blueprint.route('/empty', methods=['PUT'])(empty_cart) 

# checkout with shopping cart (shopping cart is deleted once order is processed)
shopping_cart_blueprint.route('/checkout', methods=['DELETE'])(checkout) 

# resume shopping with cart at id
shopping_cart_blueprint.route('/<shopping_cart_id>', methods=['PUT'])(set_active_cart) 
