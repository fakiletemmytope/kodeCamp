
from typing import Annotated
from fastapi import FastAPI, Form, Query, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
import random
import function
import passwd
import bcrypt

app = FastAPI()
#print(passwd.EMAIL_PASSWORD)

def generate_random_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_email(subject, recipient, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = passwd.EMAIL_ADDRESS
    msg['To'] = recipient

    mail = smtplib.SMTP('smtp.gmail.com', 465)    
    mail.ehlo()
    mail.starttls()
    mail.login(passwd.EMAIL_ADDRESS, '3JF8”5@”6')
    mail.send_message(msg)


# 1. Simple Blog Post Creation:
# Create an API endpoint that accepts a POST request with form data for blog post title, content, and author (optional).
# Validate the data using Pydantic models (ensure title and content are present, author can be optional).
# Save the blog post data and return a 201 Created response with a response model containing the created post details (ID, title, content, author).
# If validation fails, return a 400 Bad Request response with an error model containing specific details about the invalid data.

class BlogPost(BaseModel):
    title: str
    content: str
    author: str | None   

@app.post('/blog/', response_model=BlogPost, status_code=201)
async def create_blog(author: str = Form(None), title: str = Form(...), content: str = Form(...)):
    if title is None or content is None:
        raise HTTPException(status_code=400, detail='Title and Content fields are required')
    return JSONResponse(content={"title": title, "content": content, "author": author})


# 2. User Profile Update with Image Upload:
# Design an API endpoint that allows users to update their profile information (name, email) and upload an avatar image.
# Use form data for name and email, and UploadFile for the image.
# Validate the received data (e.g., name length, email format).
# Perform image size and format validation (e.g., JPEG, PNG).
# Update user information and save the uploaded image.
# Return a 200 OK response with a response model containing the updated user details (including image URL).
# Use a 400 Bad Request response with an error model for invalid data or image format.
class UserDetails(BaseModel):
    name: str
    email: EmailStr
    file: bytes 
        
    
@app.post('/user/', response_model=UserDetails, status_code=200)
def user_profile( name: str = Form(...),  email:  EmailStr = Form(...), file: UploadFile = File(...)):
    
    if len(name) > 20 or len(name) < 4:
        raise HTTPException(status_code=400, detail="Name should >= 4 and <= 20")
    
    # Validate file size
    max_file_size = 5 * 1024 * 1024  # 5 MB
    if file.content_length > max_file_size:
        raise HTTPException(status_code=400, detail="File size exceeds 5 MB")
        
    allowed_file_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_file_types:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only JPEG and PNG images are allowed")
    
    return JSONResponse(content={'name': name, 'email': email, 'file': file.filename})
    

 

# 3. Product Search with Pagination and Filtering:
# Develop an API endpoint that accepts a GET request with query parameters for product search (search term, category, price range).
# Allow optional pagination parameters (page number, page size).
# Validate and sanitize search terms on the server-side (prevent SQL injection).
# Perform product search based on criteria and pagination.
# Return a 200 OK response with a response model containing a list of matching products and pagination information (total results, current page, etc.).
# Use a 400 Bad Request response with an error model for invalid parameters or query syntax errors.


@app.get('/search/{page_number}/{page_size}')
def search(name: str, category: str, price: float, page_number: int | None, page_size: int | None):
    pass    

 

# 4. Secure Registration with OTP Verification:
# Implement an API endpoint for user registration using a POST request with form data for email, password, and optional phone number.
# Generate a secure password hash on the server-side.
# Send an OTP (One-Time Password) to the user's email or phone (using an external service).
# Return a 201 Created response with a response model containing a user ID and instructions to verify the OTP.
# Create a separate endpoint for OTP verification using a POST request with form data for OTP code.
# Validate the OTP and activate the user account.
# Return a 200 OK response with a success model or a 400 Bad Request response with an error model for invalid OTP or registration errors.
class Registration(BaseModel):
    email: EmailStr
    password: str
    phone_number: int | None
    
class Validate(BaseModel):
    email: EmailStr
    code: int
    
@app.post('/register', response_model=Registration, status_code=201)
def register(email: EmailStr = Form(...), password: str = Form(..., max_length=15, min_length=8), phone_number: int = Form(None)):
    code = generate_random_code
    body = f'This is the registrattion code: {code}. For verification, send the code and email to "http://127.0.0.1:8000/code_validation" '
    subject = "Verification Code"  
    password = "your_password".encode()  # Convert password to bytes
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    #send_email(subject, email, body)
    code_details = {
        'email': email,
        'code': code,
        'password' : hashed_password
    }
    function.update_file(code_details)    
    return{'message': 'Check you email for the verification code and instruction'}
    
@app.post('/code_validation')
def validate(email: EmailStr = Form(...), code: int = Form(...)):
    codes = function.load_file()
    initial_length = len(codes)
    new_codes = function.delete(codes, code, email)
    new_length = len(new_codes)
    if initial_length == new_length:
        return{'message': "code does not exist, registration not verified"}
    else:
        function.update_file(new_codes)
        return{'message': "registration verified"}


# 5. E-commerce Shopping Cart Management:
# Build API endpoints for managing a shopping cart:
# Adding items to the cart (POST with form data for product ID and quantity).
# Removing items from the cart (DELETE with query parameter for product ID).
# Updating item quantities in the cart (PUT with form data for product ID and updated quantity).
# Use Pydantic models to represent cart items and validate data.
# Handle cart item limits and stock availability.
# Return a 200 OK response with a success model or a 400 Bad Request response with an error model for invalid product IDs or quantity updates.
cart = []
class ProductDetails(BaseModel):
    quantity: int
    product_id: int

@app.post('/cart', response_model=ProductDetails, status_code=200) 
def add_item(quantity: int=Form(...), product_id: int =Form(...)):
    # Validate product_id and quantity
    if product_id <= 0 or quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid product ID or quantity (must be positive integers)")
        
    product_details = {
        'quantity': quantity, 'product_id':product_id
    }
    cart.append(product_details)    

    return JSONResponse(content=cart)

@app.put('/cart', response_model=ProductDetails, status_code=200)
def update_item(product_id: int = Form(...), quantity: int = Form(...)):
      

    if product_id <= 0 or quantity <= 0:         
        raise HTTPException(status_code=400, detail="Invalid product ID or quantity (must be positive integers)")
        
    for product in cart:
        if product['product_id'] == product_id:
            product['quantity'] = quantity
            return JSONResponse(content=cart)
    raise HTTPException(status_code=404, detail="No product id found")       
    
    
   
@app.delete('/cart')
def delete_item(id: int):
    if id >= 1:
        for product in cart:
            if product['product_id'] == id:
                cart.remove(product)
                return JSONResponse(content=cart)
    
    raise HTTPException(status_code=404, detail="Product not found")