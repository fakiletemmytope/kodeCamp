from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DECIMAL, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .db_connect import Base, engine
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    hashed_password = Column(String(255))
    is_admin = Column(Boolean, default=False)

    # blogs = relationship("Item", back_populates="owner")
    
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    body = Column(String(255))
    author_name = Column(String(255))
    author_id = Column(Integer)
    
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    is_published = Column(Boolean, default=False)
    description = Column(String(255))
    author_name = Column(String(255))
    author_id = Column(Integer)
    
    
class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    products = relationship("Product", back_populates="category")
    
class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    category = relationship("Category", back_populates="products")
    
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    order_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    status = Column(Enum('pending', 'completed', 'shipped', 'canceled'), default='pending')
    total_amount = Column(DECIMAL(10, 2), nullable=False)

    customer = relationship("Customer", back_populates="orders")

Base.metadata.create_all(bind=engine)

    
    
# class Category(Base):
#     __tablename__ = 'categories'

#     category_id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(255), nullable=False, unique=True)
#     description = Column(Text)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
#     updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

#     products = relationship("Product", back_populates="category")

# # Product Model
# class Product(Base):
#     __tablename__ = 'products'

#     product_id = Column(Integer, primary_key=True, autoincrement=True)
#     category_id = Column(Integer, ForeignKey('categories.category_id'))
#     name = Column(String(255), nullable=False)
#     description = Column(Text(255))
#     price = Column(DECIMAL(10, 2), nullable=False)
#     stock = Column(Integer, nullable=False)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
#     updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

#     category = relationship("Category", back_populates="products")
#     # order_items = relationship("OrderItem", back_populates="product")
#     # reviews = relationship("Review", back_populates="product")
#     # images = relationship("ProductImage", back_populates="product")
#     # cart_items = relationship("CartItem", back_populates="product")

# # Customer Model
# class Customer(Base):
#     __tablename__ = 'customers'

#     customer_id = Column(Integer, primary_key=True, autoincrement=True)
#     first_name = Column(String(255), nullable=False)
#     last_name = Column(String(255), nullable=False)
#     email = Column(String(255), nullable=False, unique=True)
#     password_hash = Column(String(255), nullable=False)
#     # phone = Column(String(20))
#     # address = Column(Text)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
#     updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

#     orders = relationship("Order", back_populates="customer")
#     # reviews = relationship("Review", back_populates="customer")
#     # cart = relationship("Cart", uselist=False, back_populates="customer")

# # Order Model
# class Order(Base):
#     __tablename__ = 'orders'

#     order_id = Column(Integer, primary_key=True, autoincrement=True)
#     customer_id = Column(Integer, ForeignKey('customers.customer_id'))
#     order_date = Column(TIMESTAMP, server_default=func.current_timestamp())
#     status = Column(Enum('pending', 'completed', 'shipped', 'canceled'), default='pending')
#     total_amount = Column(DECIMAL(10, 2), nullable=False)

#     customer = relationship("Customer", back_populates="order")
#     # order_items = relationship("OrderItem", back_populates="order")

# # OrderItem Model
# # class OrderItem(Base):
# #     __tablename__ = 'order_items'

# #     order_item_id = Column(Integer, primary_key=True, autoincrement=True)
# #     order_id = Column(Integer, ForeignKey('orders.order_id'))
# #     product_id = Column(Integer, ForeignKey('products.product_id'))
# #     quantity = Column(Integer, nullable=False)
# #     price = Column(DECIMAL(10, 2), nullable=False)

# #     order = relationship("Order", back_populates="order_items")
# #     product = relationship("Product", back_populates="order_items")

# # Review Model
# # class Review(Base):
# #     __tablename__ = 'reviews'

# #     review_id = Column(Integer, primary_key=True, autoincrement=True)
# #     product_id = Column(Integer, ForeignKey('products.product_id'))
# #     customer_id = Column(Integer, ForeignKey('customers.customer_id'))
# #     rating = Column(Integer, nullable=False)
# #     comment = Column(Text)
# #     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

# #     product = relationship("Product", back_populates="reviews")
# #     customer = relationship("Customer", back_populates="reviews")

# # Cart Model
# # class Cart(Base):
# #     __tablename__ = 'cart'

# #     cart_id = Column(Integer, primary_key=True, autoincrement=True)
# #     customer_id = Column(Integer, ForeignKey('customers.customer_id'))
# #     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

# #     customer = relationship("Customer", back_populates="cart")
# #     cart_items = relationship("CartItem", back_populates="cart")

# # CartItem Model
# # class CartItem(Base):
# #     __tablename__ = 'cart_items'

# #     cart_item_id = Column(Integer, primary_key=True, autoincrement=True)
# #     cart_id = Column(Integer, ForeignKey('cart.cart_id'))
# #     product_id = Column(Integer, ForeignKey('products.product_id'))
# #     quantity = Column(Integer, nullable=False)

# #     cart = relationship("Cart", back_populates="cart_items")
# #     product = relationship("Product", back_populates="cart_items")

# # ProductImage Model
# # class ProductImage(Base):
# #     __tablename__ = 'product_images'

# #     image_id = Column(Integer, primary_key=True, autoincrement=True)
# #     product_id = Column(Integer, ForeignKey('products.product_id'))
# #     image_url = Column(String(255), nullable=False)
# #     alt_text = Column(String(255))

# #     product = relationship("Product", back_populates="images")

      
