from fastapi import FastAPI, Query
from typing import Annotated
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


class Address(BaseModel):
    street:str
    city: str
    zip: int
    
class User_details(BaseModel):
    name: str
    email: str
    address: Address

#Task 1: Basic Query Parameters

@app.get("/items/")
def basic_query_params(name:str, category:str, price:float):
    data = {
                'name': name,
                'category': category,
                'price': price
            }
    
    return JSONResponse(content=data)
    

# Task 2: Query Parameters with Default Values and Optional Fields
# Description: Create an endpoint that uses query parameters with default values and optional fields.
# Details:
# Endpoint: /search/
# Query Parameters: query, page, size
# Return a JSON response with the search results and pagination info.

@app.get('/search')
def optional_query_parameter(query: str | None = 'name', page:int | None= 1, size: float | None = 6.8):
    
    data={'query': query, 'page': page, 'size': size} 
    
    return JSONResponse(content=data)
    
    
    
# Task 3: Request Body with Nested Pydantic Models
# Description: Create an endpoint that accepts a complex JSON request body with nested Pydantic models.
# Details:

# Endpoint: /users/
# Request Body: Pydantic model with nested fields for address and profile
# User: name, email, address: Address
# Address: street, city, zip
# Return the received data as JSON.

@app.post('/users/')
def user_info(user: User_details):
    user_details = user.__dict__
    user_info ={
        'name': user_details['name'],
        'email': user_details['email'],
        'address': user_details['address'].__dict__,
    }
    # print(user)
    return JSONResponse(content=user_info)
    

# Task 4: Query Parameters with String Validations
# Description: Create an endpoint that validates query parameters using string validations that includes length and regex.

# Details:

# Endpoint: /validate/
# Query Parameters: username
# Return a JSON response confirming the validation.
@app.get('/validate/')
def validate_parameter(username: Annotated[str, Query(min_length=6, max_length=10, pattern="[A-Z].*[a-z].*\d.*[\W_]|.*[A-Z].*[0-9].*[\W_]|.*[a-z].*[A-Z].*\d.*[\W_]|.*[a-z].*[0-9].*[\W_]|.*\d.*[A-Z].*[a-z].*[\W_]|.*\d.*[a-z].*[A-Z].*[\W_]|.*[\W_].*[A-Z].*[a-z].*\d|.*[\W_].*[a-z].*[A-Z].*\d|.*[\W_].*[a-z].*\d.*[A-Z]")]):
    
    return JSONResponse(content={'message': f"{username} is validated"})

 

# Task 5: Combined Parameters and Validations
# Description: Create an endpoint that combines path parameters, query parameters, and request body with validations.

# Details:

# Endpoint: /reports/{report_id}
# Path Parameter: report_id (must be positive)
# Query Parameters: start_date, end_date
# Request Body: Pydantic model with fields: title, content
# Return a JSON response summarizing all the received data.
class Report(BaseModel):
    title: str
    content: str
    
@app.post('/reports/{report_id}')
def combined_parameter(report_id: int, start_date: str, end_date: str, report: Report):
    
    data = {
        'id': report_id,
        'title': report.__dict__['title'],
        'content': report.__dict__['content'],
        'start': start_date,
        'end': end_date        
    }
    
    return JSONResponse(content=data)
    
