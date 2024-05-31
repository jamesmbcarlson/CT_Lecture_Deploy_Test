from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from database import db
from models.product import Product

# Create new product
def create_product(product_data):
    with Session(db.engine) as session:
        with session.begin():
            new_product = Product(
                name=product_data['name'], 
                price=product_data['price'],
                stock_quantity=product_data['stock_quantity'])
            session.add(new_product)
            session.commit()
        session.refresh(new_product)
        return new_product
    
    
# Get all products in database
def find_all(page=1, per_page=10):
    query = db.select(Product).limit(per_page).offset((page-1)*per_page)
    products = db.session.execute(query).scalars().all()
    return products

# Get one product by ID
def get_product(product_id):
    return db.session.get(Product, product_id)

# Update product at id
def update_product(product_id, product_data):
    with Session(db.engine) as session:
        with session.begin():

            # find product to update
            product_query = select(Product).where(Product.id == product_id)
            product = session.execute(product_query).scalars().first()
            if product is None:
                raise NoResultFound(f"Product could not be found with ID {product_id}")
            
            # update data for specified product
            if 'name' in product_data:
                product.name = product_data['name']
            if 'price' in product_data:
                product.price = product_data['price']
            if 'stock_quantity' in product_data:
                product.stock_quantity = product_data['stock_quantity']
            session.commit()
        session.refresh(product)
        return product

# delete product from table
def delete_product(product_id):
    with Session(db.engine) as session:
        with session.begin():
            # find product to delete
            product_query = select(Product).where(Product.id == product_id)
            product_to_delete = session.execute(product_query).scalars().first()
            if product_to_delete is None:
                raise NoResultFound(f"Product could not be found with ID {product_id}")
            # delete product if found
            session.delete(product_to_delete)
            session.commit()