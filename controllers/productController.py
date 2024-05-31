from flask import request, jsonify
from sqlalchemy.exc import NoResultFound
from schemas.productSchema import product_schema, products_schema, product_update_schema
from services import productService
from marshmallow import ValidationError
from caching import cache
from auth import login_required

# create new product
@login_required
def create_product():
    try:
        # Validate and deserialize the request data
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Call the save service with the product data
    product_save = productService.create_product(product_data)
    # Check to see that the product_save is a product and not None
    if product_save is not None:
        # Serialize the product data and return with a 201 success
        return product_schema.jsonify(product_save), 201
    else:
        return jsonify({"error": "product could not be saved"}), 400
    
# get all products
@login_required
@cache.cached(timeout=20)
def find_all():
    # get pagination parameters (or set to default)
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    products = productService.find_all(page, per_page)
    return products_schema.jsonify(products), 200

# get one product by ID
@login_required
def get_product(product_id):
    product = productService.get_product(product_id)
    if product:
        return product_schema.jsonify(product)
    else:
        resp = {
            "status": "error",
            "message": f"A product with ID {product_id} does not exist"
        }
        return resp, 404
    
# update product at id
@login_required
def update_product(product_id):
    try:
        # Validate and deserialize the request data
        update_data = product_update_schema.load(request.json)
        product_update = productService.update_product(product_id, update_data)
        return product_schema.jsonify(product_update), 201
    except (ValidationError, ValueError) as err:
        return jsonify(err.messages), 400
    except NoResultFound as err:
        return jsonify({"error": str(err)}), 404


# delete product at id
@login_required
def delete_product(product_id):
    try:
        productService.delete_product(product_id)
        response = {
            "status": "success",
            "message": f"Product with ID {product_id} has been removed"
        }
        return response, 201
    except Exception as err:
        return jsonify({"error": str(err)}), 404