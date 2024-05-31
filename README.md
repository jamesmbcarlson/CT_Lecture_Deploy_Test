## Project: Advanced E-commerce API

Author: James Carlson

This project was built as an assignment for Coding Temple.

---

<br>This E-Commerce application manages a database of <b>Customers</b>, <b>Products</b>, <b>Shopping Carts</b>, and the <b>Orders</b> of Products a Customer can place with their Shopping Cart.

## Endpoints

### <b>Login</b>
- [POST] <em>/login/</em> - Returns a token for matching username and password. A user must be logged in to access other endpoints.

### <b>Customers</b>

- [POST] <em>/customers/</em> - Add new customer.
- [GET] <em>/customers/</em> - View all customers.
- [GET] <em>/customers/{customer_id}</em> - View single customer by id.
- [PUT] <em>/customers/{customer_id}</em> - Edit customer with given id.
- [DELETE] <em>/customers/{customer_id}</em> - Delete customer with given id.

### <b>Products</b>
- [POST] <em>/products/</em> - Add new product.
- [GET] <em>/products/</em> - View all products.
- [GET] <em>/products/{product_id}</em> - View single product by id.
- [PUT] <em>/products/{product_id}</em> - Edit product with given id.
- [DELETE] <em>/products/{product_id}</em> - Delete product with given id.

### <b>Shopping Cart</b>
- [POST] <em>/cart/</em> - Create empty shopping cart.
- [GET] <em>/cart/</em> - View all shopping carts.
- [GET] <em>/cart/{cart_id}</em> - View shopping cart at id.
- [PUT] <em>/cart/add/{product_id}</em> - Add product to cart with product id.
- [PUT] <em>/cart/remove/{product_id}</em> - Remove product from cart with product id.
- [PUT] <em>/cart/update/{product_id}</em> - Update product quantity with product id.
- [PUT] <em>/cart/empty</em> - Empty cart of all products.
- [DELETE] <em>/cart/checkout</em> - Checkout with shopping cart; Order is created and Shopping Cart is deleted.
- [PUT] <em>/cart/{cart_id}</em> - Select existing cart to manage.


### <b>Orders</b>
- [GET] <em>/orders/</em> - View all orders.
- [GET] <em>/order/{order_id}</em> - View single order by id.
- [GET] <em>/order/track</em> - Track order status.

<br>
Thank you for reviewing my code!