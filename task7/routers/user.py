from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from typing import Annotated
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from ..database.db_connect import Session
from ..database.models import User
from ..utils import authenticate
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

# User Authentication and Authorization API:
# Build an API that handles user registration, login, and role-based access control. Store user credentials, roles, and permissions in an SQLite database.
router = APIRouter(
    responses={404: {"description": "Not found"}},
    tags=["users"]
)

class UserForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str  
    is_admin: bool = False

# User API:
@router.post("/user")
async def create_user(first_name:Annotated[str, Form()], last_name:Annotated[str, Form()], 
                      email:Annotated[str, Form()], password:Annotated[str, Form()], is_admin: Annotated[bool, Form()]=False):
    hash_password = bcrypt.using(rounds=13).hash(password) 
    user = User(
        first_name = first_name,
        last_name = last_name,
        email = email,
        hashed_password = hash_password,
        is_admin = is_admin
    )
    session = Session()
    try:
        session.add(user)
        session.commit()
        session.close()
        return JSONResponse(content={
         "details": "User Created"
        }, status_code=201)
    except SQLAlchemyError as e:
        session.rollback()  # Rollback the transaction on error
        return JSONResponse(
            content={
                "details": "Database error occurred",
                "error": str(e)  # Provide the error details
            },
            status_code=500  # HTTP status code for server error
        )
    except Exception as e:
        session.rollback()  # Rollback the transaction on any other errors
        return JSONResponse(
            content={
                "details": "An unexpected error occurred",
                "error": str(e)  # Provide the error details
            },
            status_code=500  # HTTP status code for server error
        )
    
@router.post("/login")
async def login(email:Annotated[str, Form()], password:Annotated[str, Form()]):
    session = Session()
    try:
        result = session.query(User).where(User.email == email).one()
        if result:
            #print(result.hashed_password)
            if authenticate.password_verification(password, result.hashed_password):
                payload = {
                    "id": result.id,
                    "username": f'{result.first_name} {result.last_name}'
                }  
                token = authenticate.get_token(payload) 
                session.close()  
                return JSONResponse(content={
                    "message": "successfully logged in",
                    "token": token
                }, status_code=200)   
            else:
                session.close()
                return JSONResponse(content=({
                    "details":  "Incorrect User login details"
                }), status_code=403)    
    except NoResultFound as e:
        session.close()
        return JSONResponse(content=({
            "details":  "User does not exists"
        }), status_code=403)
    

#user with the is_admin == false can only update his/her first and last name | user with is_admin can update any user's firstname, lastname and role
@router.put("/user")
async def update(email:Annotated[str, Form()], password:Annotated[str, Form()]):
    # session = Session()
    # result = session.query(User).where(User.email == email, User.hashed_password == password).one()
    # #print(result)
    # if result:
    #     ses
    #     return result
    # session.close()
    # return "bad"
    pass