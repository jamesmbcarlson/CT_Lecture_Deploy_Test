from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from database import db
from models.customer import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from utils.util import encode_token

# Create new customer
def create_customer(customer_data):
    with Session(db.engine) as session:
        with session.begin():
            # check if username is already in database
            customer_query = select(Customer).where(Customer.username == customer_data['username'])
            check_username = db.session.execute(customer_query).scalars().first()
            if check_username:
                raise ValueError("Username is already taken. Please create a unique username.")
            
            # add new customer to database
            new_customer = Customer(
                name=customer_data['name'], 
                email=customer_data['email'], 
                phone=customer_data['phone'],
                username=customer_data['username'],
                password=generate_password_hash(customer_data['password'])
                )
            session.add(new_customer)
            session.commit()
        session.refresh(new_customer)
        return new_customer

# Get all customers in database
def get_all(page=1, per_page=10):
    query = db.select(Customer).limit(per_page).offset((page-1)*per_page)
    customers = db.session.execute(query).scalars().all()
    return customers

# Get one customer by ID
def get_customer(customer_id):
    return db.session.get(Customer, customer_id)

# Update customer by id
def update_customer(customer_id, customer_data):
    with Session(db.engine) as session:
        with session.begin():

            # find customer to update
            customer_query = select(Customer).where(Customer.id == customer_id)
            customer = session.execute(customer_query).scalars().first()
            if customer is None:
                raise NoResultFound(f"Customer could not be found with ID {customer_id}")
            
            # update data for specified customer
            if 'name' in customer_data:
                customer.name = customer_data['name']
            if 'email' in customer_data:
                customer.email = customer_data['email']
            if 'phone' in customer_data:
                customer.phone = customer_data['phone']
            if 'username' in customer_data:
                # Check if new username is already taken by another customer
                username_query = select(Customer).where(Customer.username == customer_data['username'], Customer.id != customer_id)
                check_username = session.execute(username_query).scalars().first()
                if check_username:
                    raise ValueError("Username is already taken. Please create a unique username.")
                customer.username = customer_data['username']
            if 'password' in customer_data:
                customer.password = generate_password_hash(customer_data['password'])

            session.commit()
        session.refresh(customer)
        return customer

# delete customer from table
def delete_customer(customer_id):
    with Session(db.engine) as session:
        with session.begin():
            # find customer to delete
            customer_query = select(Customer).where(Customer.id == customer_id)
            customer_to_delete = session.execute(customer_query).scalars().first()
            if customer_to_delete is None:
                raise NoResultFound(f"Customer could not be found with ID {customer_id}")
            # delete customer if found
            session.delete(customer_to_delete)
            session.commit()

# return token for valid login
def get_token(username, password):
    # query the customer table for given username
    query = db.select(Customer).where(Customer.username == username)
    customer = db.session.execute(query).scalars().first()
    # validate password for paired username
    if customer is not None and check_password_hash(customer.password, password):
        print("CUSTOMER ID", customer.id)
        auth_token = encode_token(customer.id)
        return auth_token
    else:
        return None