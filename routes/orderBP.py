from flask import Blueprint
from controllers.orderController import create_order, find_all, get_order, track_order

order_blueprint = Blueprint("order_bp", __name__)

# order_blueprint.route('/', methods=['POST'])(create_order) # in this application, orders are created via the shoppingCartService checkout method 
order_blueprint.route('/', methods=['GET'])(find_all)
order_blueprint.route('/<order_id>', methods=['GET'])(get_order) # view order at id
order_blueprint.route('/track/<order_id>', methods=['GET'])(track_order)

# view all orders for customer id
# '/customer/<customer_id>'

# order_blueprint.route('/cancel/<order_id>', methods=['PUT'])() # cancel order at id