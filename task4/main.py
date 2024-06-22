from typing import Annotated
from fastapi import FastAPI, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import time
import requests
import random

app = FastAPI()

class Parameters(BaseModel):
    number1: int
    number2: int
    operator: str

class Name(BaseModel):
    Firstname: str
    Lastname: str
    

#Calculator dependency
async def operation(number1: Annotated[int , Form()], number2: Annotated[int, Form()], operator: Annotated[str, Form()]):
    operators = ["add", "ADD", "Add", "Sub", "sub", "SUB", "mul", "MUL", "Mul", "div", "DIV", "Div"]
    if operator.lower() in operators:        
        if operator.lower() == 'add' :
            result = number1 + number2
        elif operator.lower() == 'sub':
            result = number1 - number2
        elif operator.lower() == 'mul':
            result =  number1 * number2
        else:
            return number1/number2
    else:
        result = {"details": "Invalid operator, operator should be 'div', 'sub', 'add' or 'mul'"}
    return result

#greeting dependency
async def getTimeOfTheDay():
    hour_of_day = time.localtime().tm_hour
    if hour_of_day >= 6 and hour_of_day < 12:
        return "morning"
    elif hour_of_day >= 12 and hour_of_day < 18:
        return "afternon"
    elif hour_of_day >= 18 and hour_of_day < 24:
        return "Evening"
    else:
        return "night"
    
#booksearch dependency
async def search(q: str):
    books = []
    if q:
        url = f'https://www.googleapis.com/books/v1/volumes?q={q}'        
        response = requests.get(url)
        if response:
            response_dict = response.json()
            items = response_dict['items']
            if items:            
                for item in items:
                    book = {}
                    bookInfo = item.get('volumeInfo',{})
                    book['title'] = bookInfo.get('title', None)
                    book['authors'] = bookInfo.get('authors', [])
                
                    book['publisher'] = bookInfo.get('publisher', None)
                
                    book['publishedDate'] = bookInfo.get('publishedDate', None)
                
                    book['language'] = bookInfo.get('language', None)
                
                    book['pageCount']= bookInfo.get('pageCount', None)
                    books.append(book)
                    print(book)
        else:
            return "Error in network connection"
    return books   

async def flag():
    # Your list of two items
    role = ["Admin", "user"]
    # Select a random index from 0 (inclusive) to the length of the list minus 1 (exclusive)
    random_index = random.randrange(len(role))
    # Pick the item at the random index
    return role[random_index]

# 1. Dependency Injected Calculator API:
# Create a simple calculator API where arithmetic operations (addition, subtraction, multiplication, division) are performed using dependency-injected functions.
@app.post('/calculator/', response_model=Parameters)
async def calculate(result: Annotated[float | int | dict, Depends(operation)]):
    return JSONResponse(content={"result": result})


# 2. Configurable Greeting API:
# Build an API that returns a greeting message. Use dependencies to inject different greeting messages based on the time of day
@app.get('/greetings/')
async def greet(time: Annotated[str, Depends(getTimeOfTheDay)]):
    greet = f'Good {time}, Visitor'
    return JSONResponse(content={"message": greet})


# 3.Configurable Feature Flags API:
# Build an API that uses feature flags to enable or disable features. Use dependencies to inject the current state of feature flags into your endpoints.
@app.post('/info', response_model=Name)
async def info(Firstname: Annotated[str, Form()], Lastname: Annotated[str, Form()], flag: Annotated[str, Depends(flag)]):
    if flag == 'Admin':
        return JSONResponse(content={'message' : f"{Firstname} {Lastname} you are logged in as an Admin"})
    if flag == "user":
        return JSONResponse(content={'message' : f"{Lastname} {Firstname} you are logged in as User"})
        
 

 
# 4. Third-Party API Integration:
# Build an API that integrates with a third-party service (e.g., weather API). Use dependencies to handle the setup and configuration of the third-party client
@app.get('/search')
async def searchbook(result: Annotated[str|list, Depends(search)]):
    return JSONResponse(content={'books': result})