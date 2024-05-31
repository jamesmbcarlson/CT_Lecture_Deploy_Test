from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from sqlalchemy.exc import NoResultFound
from database import db
import datetime
from models.order import Order
from models.customer import Customer
from models.product import Product
from models.shoppingCart import ShoppingCart
from models.shoppingCartProducts import shopping_cart_products
from models.orderProducts import order_products
from services.productService import get_product
from services.orderService import set_delivery_date

# current_cart is the cart_id functions should be managing
current_cart = -1

def set_current_cart(id):
    global current_cart
    current_cart = id
    return

def get_current_cart():
    global current_cart
    if int(current_cart) < 0:
        raise ValueError("No shopping cart in use.")
    return current_cart

# Creates new shopping_cart
def create_cart(customer_id):
    with Session(db.engine) as session:
        with session.begin():
            # Check that the customer_id is associated with a customer
            customer = session.get(Customer, customer_id)
            if not customer:
                raise ValueError(f"Customer with ID {customer_id} does not exist")
            # Create a new shopping_cart in the database
            new_shopping_cart = ShoppingCart(customer_id=customer_id)
            session.add(new_shopping_cart)
            session.commit()

        session.refresh(new_shopping_cart)
        set_current_cart(new_shopping_cart.id)
        return

# Get one cart by ID
def get_cart(cart_id):
    return db.session.get(ShoppingCart, cart_id)

# add item to current cart by product ID
def add_to_cart(product_id):
    cart_id = get_current_cart()
    print("CURRENT CART ID:", cart_id) # DEBUG

    # add product to join table; if already in, increment quantity
    with Session(db.engine) as session:
        with session.begin():

            # check if product is valid
            product = get_product(product_id)
            if product is None:
                raise NoResultFound("Product not found")

            # check stock quantity before adding product
            if int(product.stock_quantity) > 0:
                product.stock_quantity = int(product.stock_quantity) - 1
                    
                # get cart/product row in join table, if it exists
                cart_query = select(shopping_cart_products).where(
                    and_(
                        shopping_cart_products.c.shopping_cart_id == cart_id,
                        shopping_cart_products.c.product_id == product_id))
                product_in_cart = db.session.execute(cart_query).fetchone()

                # if product is already in cart, increase quantity
                if product_in_cart:
                    update_statement = shopping_cart_products.update().where(
                        and_(
                            shopping_cart_products.c.shopping_cart_id == cart_id,
                            shopping_cart_products.c.product_id == product_id)).values(quantity=int(product_in_cart[2]) + 1) # product_in_cart[2] = 'quantity'
                    db.session.execute(update_statement)
                # if product is not in cart, add it
                else:
                    add_new_item_statement = shopping_cart_products.insert().values(
                        shopping_cart_id=cart_id,
                        product_id=product_id,
                        quantity=1)
                    db.session.execute(add_new_item_statement)
                db.session.commit()
                return
            else:
                raise ValueError("Not enough products in stock")
    
# remove item from current cart by product ID
def remove_from_cart(product_id):
    cart_id = get_current_cart()

    # decrement quantity in join table; if zero, remove product
    with Session(db.engine) as session:
        with session.begin():

            # check if product is valid
            product = get_product(product_id)
            if product is None:
                raise NoResultFound(f"Error: Product not found with ID {product_id}")
        
            # get cart/product row in join table, if it exists
            cart_query = select(shopping_cart_products).where(
                and_(
                    shopping_cart_products.c.shopping_cart_id == cart_id,
                    shopping_cart_products.c.product_id == product_id))
            product_in_cart = db.session.execute(cart_query).fetchone()

            # if product is in cart, decrease quantity
            if product_in_cart:
                new_quantity=int(product_in_cart[2]) - 1 # product_in_cart[2] = 'quantity'

                # delete join table row if quantity reaches 0
                if(new_quantity <= 0):
                    delete_statement = shopping_cart_products.delete().where(
                        and_(
                            shopping_cart_products.c.shopping_cart_id == cart_id,
                            shopping_cart_products.c.product_id == product_id))
                    db.session.execute(delete_statement)

                # update quantity for product in cart
                else:
                    update_statement = shopping_cart_products.update().where(
                        and_(
                            shopping_cart_products.c.shopping_cart_id == cart_id,
                            shopping_cart_products.c.product_id == product_id)).values(quantity=new_quantity)
                    db.session.execute(update_statement)
                db.session.commit()

            # if product is not in cart, throw exception
            else:
                raise NoResultFound("Error: Product not in cart.")


# update item quantity in current cart by product ID
def update_item_qty(product_id, update_data):
    cart_id = get_current_cart()
    new_quantity = int(update_data['quantity'])

    # update quantity with json for product_id in join table
    with Session(db.engine) as session:
        with session.begin():

            # check if product is valid
            product = get_product(product_id)
            if product is None:
                raise NoResultFound("Product not found")
                    
            # get cart/product row in join table, if it exists
            cart_query = select(shopping_cart_products).where(
                and_(
                    shopping_cart_products.c.shopping_cart_id == cart_id,
                    shopping_cart_products.c.product_id == product_id))
            product_in_cart = db.session.execute(cart_query).fetchone()

            # if product is already in cart, adjust quantity
            if product_in_cart:
                adjusted_stock_quantity = int(product.stock_quantity) + int(product_in_cart[2]) # product_in_cart[2] = 'quantity'

                # if new quantity is 0, delete row
                if(new_quantity <= 0):
                    delete_statement = shopping_cart_products.delete().where(
                        and_(
                            shopping_cart_products.c.shopping_cart_id == cart_id,
                            shopping_cart_products.c.product_id == product_id))
                    db.session.execute(delete_statement)
                    db.session.commit()
                    product.stock_quantity = adjusted_stock_quantity
                    return

                # check stock quantity before updating quantity
                if adjusted_stock_quantity >= new_quantity:
                    product.stock_quantity = adjusted_stock_quantity - new_quantity

                update_statement = (shopping_cart_products.update().where(
                    and_(
                        shopping_cart_products.c.shopping_cart_id == cart_id,
                        shopping_cart_products.c.product_id == product_id)).values(quantity=new_quantity)) 
                db.session.execute(update_statement)

            # if product is not in cart, add it
            else:
                add_new_item_statement = shopping_cart_products.insert().values(
                    shopping_cart_id=cart_id,
                    product_id=product_id,
                    quantity=1)
                db.session.execute(add_new_item_statement)
            db.session.commit()


# remove all products in cart
def empty_cart():
    cart_id = get_current_cart()

    # remove all products and quantities from join table, restock products
    with Session(db.engine) as session:
        with session.begin():
            # restock products from cart
            cart_query = select(shopping_cart_products).where(
                shopping_cart_products.c.shopping_cart_id == cart_id)
            products_in_cart = session.execute(cart_query).fetchall()
            for p in products_in_cart:
                restock_query = select(Product).where(Product.id == p[1])
                product = session.execute(restock_query).scalars().first() 
                if product is None:
                    raise NoResultFound(f"Error: Product not found")
                product.stock_quantity = int(product.stock_quantity) + int(p[2])

            # delete all rows of join table
            delete_statement = shopping_cart_products.delete().where(
                shopping_cart_products.c.shopping_cart_id == cart_id)
            session.execute(delete_statement)
            session.commit()

# place order with shopping cart data
def checkout():
    cart_id = get_current_cart()
    cart = get_cart(cart_id)
    product_data = []
    new_order = None

    # transfer shopping cart to order
    with Session(db.engine) as session:
        with session.begin():
            
            # get total price of cart
            total_price = 0.0
            cart_query = select(shopping_cart_products).where(
                shopping_cart_products.c.shopping_cart_id == cart_id)
            products_in_cart = session.execute(cart_query).fetchall()
            for p in products_in_cart:
                query = select(Product).where(Product.id == p[1])
                product = session.execute(query).scalars().first() 
                if product is None:
                    raise NoResultFound(f"Error: Product not found")
                total_price += (float(product.price) * int(p[2]))

                # create data copies for order_products table
                product_data.append((p[1], p[2]))


            order_date = datetime.datetime.today().date()
            delivery_date = set_delivery_date(order_date)

            # transfer cart data to new order object
            new_order = Order(
                customer_id=cart.customer_id,
                order_date=order_date,
                delivery_date=delivery_date,
                total_price=total_price,
                cancelled=False)
            session.add(new_order)

            # delete cart
            delete_query = select(ShoppingCart).where(ShoppingCart.id == cart_id)
            cart_to_delete = session.execute(delete_query).scalars().first()
            if cart_to_delete is None:
                raise NoResultFound(f"Shopping cart could not be found with ID {cart_id}")
            # delete shopping cart
            session.delete(cart_to_delete)
            set_current_cart(-1)

            session.commit()
        session.refresh(new_order)      

    with Session(db.engine) as session:
        with session.begin():
            # copy data from cart_product join table to order_product join table
            for data in product_data:
                add_new_order_prd_statement = order_products.insert().values(
                        order_id=new_order.id,
                        product_id=data[0],
                        quantity=data[1])
                session.execute(add_new_order_prd_statement)  
            session.commit()

# Get all shopping_carts in database
def find_all(page=1, per_page=10):
    query = db.select(ShoppingCart).limit(per_page).offset((page-1)*per_page)
    orders = db.session.execute(query).scalars().all()
    return orders
