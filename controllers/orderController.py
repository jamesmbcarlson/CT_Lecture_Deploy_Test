from flask import request, jsonify
from sqlalchemy.exc import NoResultFound
from schemas.orderSchema import order_schema, orders_schema
from services import orderService
from marshmallow import ValidationError
from caching import cache
from auth import login_required

# place order / create new order
# in this application, orders are placed via the shoppingCartService checkout method
@login_required
def create_order():
    pass
    # try:
    #     raw_data = request.json
    #     logged_in_user = token_auth.current_user()
    #     raw_data['customer_id'] = logged_in_user.id
    #     order_data = order_schema.load(raw_data)
    #     order_save = orderService.create_order(order_data)
    #     return order_schema.jsonify(order_save), 201
    # except ValidationError as err:
    #     return jsonify(err.messages), 400
    # except ValueError as err:
    #     return jsonify({'error': str(err)}), 400

# get all orders
@cache.cached(timeout=20)
@login_required
def find_all():
    # get pagination parameters (or set to default)
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    orders = orderService.find_all(page, per_page)
    return orders_schema.jsonify(orders), 200

# get one order by ID
@login_required
def get_order(order_id):
    order = orderService.get_order(order_id)
    if order:
        return order_schema.jsonify(order)
    else:
        resp = {
            "status": "error",
            "message": f"A order with ID {order_id} does not exist"
        }
        return resp, 404

# get status of order by id
@login_required
def track_order(order_id):
    try:
        return orderService.track_order(order_id)
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404



# TO-DO: 
# Manage Order History (Bonus): Create an endpoint that allows customers to access their order history, listing all previous orders placed. Each order entry should provide comprehensive information, including the order date and associated products.
    # take in customer ID, return list of orders
# Cancel Order (Bonus): Implement an order cancellation feature, allowing customers to cancel an order if it hasn't been shipped or completed. Ensure that canceled orders are appropriately reflected in the system.
    # take in order ID, set cancellation of order to false if not shipped or already completed