from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from database import db
import datetime, random
from models.order import Order
from models.customer import Customer
from models.product import Product

# in this application, orders are placed via the shoppingCartService checkout method
def create_order(order_data):
    pass
    # with Session(db.engine) as session:
    #     with session.begin():
    #         # Check that the customer_id is associated with a customer
    #         customer_id = order_data['customer_id']
    #         customer = session.get(Customer, customer_id)
    #         if not customer:
    #             raise ValueError(f"Customer with ID {customer_id} does not exist")

    #         # Get all of the product_ids from the order_data products
    #         product_ids = [prod['id'] for prod in order_data['products']]
    #         product_query = select(Product).where(Product.id.in_(product_ids))
    #         products = session.execute(product_query).scalars().all()
    #         # Make sure all of the products exist and were queried
    #         if len(product_ids) != len(products):
    #             raise ValueError("One or more products do not exist")
            
    #         # TO-DO: handle quantity for products
    #         # note - maybe orders can only be created via shopping cart

    #         # set order date to current date, randomize delivery date
    #         order_date = datetime.today()
    #         estimated_delivery_span = random.randint(2,5)
    #         delivery_date = order_date + datetime.timedelta(days=estimated_delivery_span)
    #             # if delivery date is a Sunday, deliver next day; no deliveries on Sundays!
    #         if delivery_date.weekday() == 6:
    #             delivery_date += datetime.timedelta(days=1)

    #         # total_price
    #         # note - total_price should be set calculating product prices times quantity, so I need that quantity column to be active somehow

    #         # Create a new order in the database
    #         new_order = Order(
    #             customer_id=order_data['customer_id'],
    #             products=products,
    #             order_date=order_date,
    #             delivery_date=delivery_date)
    #         session.add(new_order)
    #         session.commit()

    #     session.refresh(new_order)

    #     for product in new_order.products:
    #         session.refresh(product)

    #     return new_order
    
# Get all orders in database
def find_all(page=1, per_page=10):
    query = db.select(Order).limit(per_page).offset((page-1)*per_page)
    orders = db.session.execute(query).scalars().all()
    return orders

# Get one order by ID
def get_order(order_id):
    return db.session.get(Order, order_id)

# set randomized delivery date
def set_delivery_date(order_date):
    estimated_delivery_span = random.randint(2,5)
    delivery_date = order_date + datetime.timedelta(days=estimated_delivery_span)
        # if delivery date is a Sunday, deliver next day; no deliveries on Sundays!
    if delivery_date.weekday() == 6:
        delivery_date += datetime.timedelta(days=1)
    return delivery_date

# get status of order by id
def track_order(order_id):
    with Session(db.engine) as session:
        with session.begin():

            # find order to track
            order_query = select(Order).where(Order.id == order_id)
            order = session.execute(order_query).scalars().first()
            if order is None:
                raise NoResultFound(f"Order could not be found with ID {order_id}")
            
            order_date = order.order_date
            delivery_date = order.delivery_date

            # get status of order
            if order.cancelled:
                return f"Your order (ID {order_id}) from {order_date} has been cancelled"

            elif order.delivery_date < datetime.date.today():
                return f"Your order (ID {order_id}) from {order_date} was delivered on {delivery_date}!"
            
            elif order.delivery_date == datetime.date.today():
                return f"Your order (ID {order_id}) from {order_date} will arrive today!"
            
            else:
                return f"Your order (ID {order_id}) from {order_date} is on its way! Estimated delivery: {delivery_date}"


# TO-DO: 
    # view all orders for customer id
    # cancel order