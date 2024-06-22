from typing import Annotated
from fastapi import FastAPI, Form, Query, Depends,  UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import time

app = FastAPI()

class Parameters(BaseModel):
    number1: int
    number2: int
    operator: str
    

# 1. Dependency Injected Calculator API:
# Create a simple calculator API where arithmetic operations (addition, subtraction, multiplication, division) are performed using dependency-injected functions.
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

async def getTimeOfTheDay():
    hour_of_day = time.localtime().tm_hour
    if hour_of_day >= 6 or hour_of_day <= 11:
        return "morning"
    elif hour_of_day >= 12 or hour_of_day <= 17:
        return "afternon"
    elif hour_of_day >= 18 or hour_of_day <= 24:
        return "Evening"
    else:
        return "night"

@app.post('/calculator/')
async def calculate(result: Annotated[float | int | dict, Depends(operation)]):
    return JSONResponse(content={"result": result})

# 2. Configurable Greeting API:
# Build an API that returns a greeting message. Use dependencies to inject different greeting messages based on the time of day
@app.get('/greetings/')
async def greet(time: Annotated[str, Depends(getTimeOfTheDay)]):
    return f'Good {time}, Visitor'

# 3.Configurable Feature Flags API:
# Build an API that uses feature flags to enable or disable features. Use dependencies to inject the current state of feature flags into your endpoints.

 

 

# 4. Third-Party API Integration:
# Build an API that integrates with a third-party service (e.g., weather API). Use dependencies to handle the setup and configuration of the third-party client
