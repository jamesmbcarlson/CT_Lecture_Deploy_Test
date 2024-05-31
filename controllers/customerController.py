from flask import request, jsonify
from sqlalchemy.exc import NoResultFound
from schemas.customerSchema import customer_input_schema, customer_output_schema, customers_schema, customer_update_schema, customer_login_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache
from auth import login_required

# create new customer
@login_required
def create_customer():
    try:
        # Validate and deserialize the request data
        customer_data = customer_input_schema.load(request.json)
        customer_save = customerService.create_customer(customer_data)
        return customer_output_schema.jsonify(customer_save), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

# get all customers
@cache.cached(timeout=20)
@login_required
def get_all():
    # get pagination parameters (or set to default)
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    customers = customerService.get_all(page, per_page)
    return customers_schema.jsonify(customers), 200

    

# get one customer by ID
@login_required
def get_customer(customer_id):
    customer = customerService.get_customer(customer_id)
    if customer:
        return customer_output_schema.jsonify(customer)
    else:
        resp = {
            "status": "error",
            "message": f"A customer with ID {customer_id} does not exist"
        }
        return resp, 404

# update customer at id
@login_required
def update_customer(customer_id):
    try:
        # Validate and deserialize the request data
        update_data = customer_update_schema.load(request.json)
        customer_update = customerService.update_customer(customer_id, update_data)
        return customer_output_schema.jsonify(customer_update), 201
    except (ValidationError, ValueError) as err:
        return jsonify(err.messages), 400
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404


# delete customer at id
@login_required
def delete_customer(customer_id):
    try:
        customerService.delete_customer(customer_id)
        response = {
            "status": "success",
            "message": f"Customer with ID {customer_id} has been removed"
        }
        return response, 201
    except Exception as err:
        return jsonify({"error": str(err)}), 404

# logging in
def login():
    try:
        customer_data = customer_login_schema.load(request.json)
        token = customerService.get_token(customer_data['username'], customer_data['password'])
        if token:
            resp = {
                "status": "success",
                "message": "You have successfully authenticated yourself",
                "token": token
            }
            return jsonify(resp), 200
        else:
            resp = {
                "status": "error",
                "message": "Username and/or password is incorrect"
            }
            return jsonify(resp), 401 # 401 - HTTP Status - Unauthorized
    except ValidationError as err:
        return jsonify(err.messages), 400