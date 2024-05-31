from flask import Blueprint
from controllers.customerController import create_customer, get_all, get_customer, update_customer, delete_customer

customer_blueprint = Blueprint("customer_bp", __name__)

customer_blueprint.route('/', methods=['POST'])(create_customer) # create customer
customer_blueprint.route('/', methods=['GET'])(get_all) # view all
customer_blueprint.route('/<customer_id>', methods=['GET'])(get_customer) # view customer at id
customer_blueprint.route('/<customer_id>', methods=['PUT'])(update_customer) # update customer at id
customer_blueprint.route('/<customer_id>', methods=['DELETE'])(delete_customer) # delete customer at id
