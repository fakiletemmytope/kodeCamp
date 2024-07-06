from fastapi import FastAPI, HTTPException, Request, Form
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.hash import bcrypt
from functions import file_update, to_do_auth

app = FastAPI()

#auth = OAuth2PasswordBearer
# OAuth2 Secured To-Do List API:
# Create a to-do list API where users can sign in with OAuth2. Use middleware to ensure only authenticated users can create, view, update, or delete tasks.

class User(BaseModel):
    username: str
    password: str
    
class Todo(BaseModel):
    username: str
    password: str
    is_complete: bool
 
@app.middleware("http")
async def authenticateUser(request: Request, call_next):
    urlpath = request.url.path
    if urlpath == "/createuser":
        response = await call_next(request)
        return response
    elif urlpath == "/todo_login":
        response = await call_next(request)
        return response
    else:
        #print(request.headers["authorization"].split(" ")[1])
        if request.headers.get("authorization"):
            decode_token = to_do_auth.authenticate_token(request.headers.get("authorization").split(" ")[1])            
            response = await call_next(request)
            return response
        else:
            return JSONResponse(content={"detail":"Unauthorized user"})
        
@app.post('/createuser', response_model=User)
async def createUser(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    path ="./todo/users.json"
    f = file_update.openfile(path)
    #print(type(f))
    for key in f:
        if key == username:
          return  JSONResponse(content={"error_message": "user already exists"}) 
    hash_password = bcrypt.using(rounds=13).hash(password) 
    new_user = {
        "username": username,
        "password": hash_password
    }  
    f[username] = new_user
    file_update.updatefile(path, f)
    return  JSONResponse(content={"message": "user created", "details":{"username":username, "password": hash_password}, "user": f})

    
@app.post('/todo_login', response_model=User)
async def signIn(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    path ="./todo/users.json"
    f = file_update.openfile(path)
    #print(type(f))
    for key in f:
        #print(key)
        if key == username:
            #print("ter")
            user_details = f[username]
            check = to_do_auth.password_verification(password, user_details['password'])
            if check is True:
                #print("true")
                token = to_do_auth.get_token(f[username])
                return JSONResponse(content={"message": "login successful", "bearer_token": token})
            else:
                #print("false")
                return JSONResponse(content={"error_message": "incorrect username or password"})
        
    #print("user error")
    return JSONResponse(content={"error_message": "incorrect username or password"}) 
    
@app.get('/todo')
async def view():
    path = './todo/todo.json'
    todo_list = file_update.openfile(path)
    return JSONResponse(content={"list": todo_list})
    
@app.post('/todo',response_model=Todo)
async def create(title: Annotated[str, Form()]):
    path = './todo/todo.json'
    f= file_update.openfile(path)
    id = len(f) + 1
    new_todo = {
        "title": title,
        "id": id,
        "created_by": to_do_auth.current_user,
        "is_complete": False
    }
    f.append(new_todo)
    file_update.updatefile(path, f)
    return JSONResponse(content=f)
    
@app.put('/todo/:id')
async def signIn(id: Annotated[int, id], title: Annotated[str | None, Form()], is_complete: Annotated[bool | None, Form()]):
    path = "./todo/todo.json"
    f = file_update.openfile(path)
    for todo in f:
        if todo["id"] == id:
            if title:
                todo["title"] = title
            if is_complete:
                todo["is_complete"] = is_complete
            file_update.updatefile(path, f)
            return JSONResponse(content={"list": f})
    return{
        'error' : 'todo does not exist'
    }

@app.delete('/todo/:id')
async def signIn(id: Annotated[int, id]):
    path = "./todo/todo.json"
    f = file_update.openfile(path)
    i = 0
    for todo in f:
        if todo["id"] == id:           
            f.remove(i)
            file_update.updatefile(path, f)
            return JSONResponse(content={"list": f})
        i = i + 1
    return{
        'error' : 'todo does not exist'
    }

# OAuth2 User Profile API:
# Develop an API where users can sign in with OAuth2 and manage their profiles. Use middleware to protect profile endpoints and allow users to update their information securely.

 

# OAuth2 Secured Notes API:
# Build a notes API with OAuth2 authentication. Use middleware to ensure that users can only access their own notes, providing a secure way to manage personal information.

 

# OAuth2 Protected Blog API:
# Create a blog API where users can log in with OAuth2 to create, edit, and delete blog posts. Use middleware to restrict actions to authenticated users only.

 

# OAuth2 E-commerce API:
# Develop an e-commerce API with OAuth2 for user authentication. Implement middleware to protect user actions like viewing order history, placing orders, and managing account details.