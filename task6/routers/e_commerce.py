# E-commerce API:
# Develop an e-commerce API to manage products, categories, orders, and customers. Use SQLite to store product details, customer information, and order histories.

#Things to do
# create customers
#all users can get all products, and products by catergory and by id but cannot post,delete or update product/category
# all users can post orders and can only get their orders
# create products and Products
# Customers can make an order


from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from database.db_connect import Session
from database.models import Customer, Order, Product, Category
from pydantic import BaseModel, EmailStr
from utils.authenticate import hash_passwd, password_verification, get_token
from sqlalchemy.exc import SQLAlchemyError
from utils.serializer import serialize


router = APIRouter(
    prefix="/ecommerce"
)

class CustomerForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class OrderForm(BaseModel):
    total_amount: float
    status: str

@router.post("/customer")
async def reg(first_name: Annotated[str, Form()], last_name: Annotated[str, Form()], password: Annotated[str, Form()], email: Annotated[EmailStr, Form()]):
    hash_passwd = hash_passwd(password)
    customer = Customer(
        first_name = first_name,
        last_name = last_name,
        password_hash = hash_passwd
    )
    try:
        session = Session()
        session.add(customer)
        session.commit()
        session.close()
        return JSONResponse(content={
            "message" : "Customer created"
        }, status_code=401)
    except SQLAlchemyError as e:
        return JSONResponse(content={
            "message" : str(e)
        }, status_code=401)
    except Exception as e:
        return JSONResponse(content={
            "message" : str(e)
        }, status_code=500)

@router.post("/login")
async def login(password: Annotated[str, Form()], email: Annotated[EmailStr, Form()]):
    try:
        session = Session()
        result = session.query(Customer).filter(Customer.email == email)
        if result and password_verification(password, result.password_hash):
            customer_data = {
                "customerId" : result.customer_id,
                "customer_name": f'{result.last_name} {result.first_name}'
            }
            token = get_token(customer_data)
            return JSONResponse(content={
                "message": "Login successfull",
                "token": token
            }, status_code=200)
        else:
            return JSONResponse(content={
                "message" : "Incorrect login details"
            }, status_code=401)
    except SQLAlchemyError as e:
        return JSONResponse(content={
            "message" : str(e)
        }, status_code=401)
    except Exception as e:
        return JSONResponse(content={
            "message" : str(e)
        }, status_code=500)
    
@router.post("/order")
async def make_order():
    pass

@router.get("/order")
async def get_all_orders(request: Request):
    custom_data = request.state.custom_data
    session = Session()
    param = ["order_id", "order_date", "status", "total_amount"]
    try:        
        result = session.query(Order).filter(Order.customer_id == custom_data.current_userId).all()
        serialized = serialize(param, result)
        return JSONResponse(content={
            "orders": serialized
        },status_code=200)
    except SQLAlchemyError as e:
        return JSONResponse(content={
            "message": str(e)
        }, status_code=401)
    except Exception as e:
        return JSONResponse(content={
            "message": str(e)
        }, status_code=500)

@router.get("/order/{order_id}")
async def get_an_order(order_id: int, request: Request):
    custom_data = request.state.custom_data
    session = Session()
    param = ["order_id", "order_date", "status", "total_amount"]
    try:
        result = session.query(Order).filter(Order.order_id == order_id, Order.customer_id == custom_data.current_userId).one()
        serialized = serialize(param, result)
        return JSONResponse(content={
            "orders": serialized
        },status_code=200)
    except SQLAlchemyError as e:
        return JSONResponse(content={
            "message": str(e)
        }, status_code=401)
    except Exception as e:
        return JSONResponse(content={
            "message": str(e)
        }, status_code=500)


