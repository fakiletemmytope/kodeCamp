from fastapi import FastAPI, HTTPException, Request, Form, Query
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.hash import bcrypt
from functions import file_update, to_do_auth
app = FastAPI()

class User(BaseModel):
    First_name: str
    Last_name: str
    Email: str
    username: str
    password: str
    
class Todo(BaseModel):
    title: str | None = None
    is_complete: bool | None = None

class Note(BaseModel):
    title: str
    body: str

class Blog(BaseModel):
    title: str
    body: str
    is_published: bool | None = None
    
@app.middleware("http")
async def authenticateUser(request: Request, call_next):
    urlpath = request.url.path
    verb = request.method
    print(verb, urlpath)
    if urlpath == "/createuser" or urlpath == "/docs":
        response = await call_next(request)
        return response
    elif urlpath == "/todo_login" or urlpath == "/user_login":
        response = await call_next(request)
        return response
    elif urlpath == "/user" and verb == "POST":
        response = await call_next(request)
        return response
    else:
        #print(request.headers["authorization"].split(" ")[1])
        if request.headers.get("authorization"):
            to_do_auth.authenticate_token(request.headers.get("authorization").split(" ")[1])            
            response = await call_next(request)
            return response
        else:
            return JSONResponse(content={"detail":"Unauthorized user"})

#auth = OAuth2PasswordBearer
# OAuth2 Secured To-Do List API:
# Create a to-do list API where users can sign in with OAuth2. Use middleware to ensure only authenticated users can create, view, update, or delete tasks.
     
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
    if title:
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
    return JSONResponse(content={"error message": "The title field must be filled"})
    
@app.put('/todo/{id}', response_model=Todo)
async def updateTodo(id: Annotated[int, id], title: Annotated[str | None, Form()] = None, is_complete: Annotated[bool , Form()]= None):
    path = "./todo/todo.json"
    f = file_update.openfile(path)
    for todo in f:
        if todo["id"] == id:
            if title:
                todo["title"] = title
            if is_complete is not None:
                todo["is_complete"] = is_complete
            file_update.updatefile(path, f)
            return JSONResponse(content={"list": f})
    return{
        'error' : 'todo does not exist'
    }

@app.delete('/todo/{id}')
async def deleteTodo(id: Annotated[int, id]):
    path = "./todo/todo.json"
    f = file_update.openfile(path)
    # i = 0
    for todo in f:
        if todo["id"] == id:         
            f.remove(todo)
            file_update.updatefile(path, f)
            return JSONResponse(content={"list": f})
        # i = i + 1
    return{
        'error' : 'todo does not exist'
    }

# OAuth2 User Profile API:
# Develop an API where users can sign in with OAuth2 and manage their profiles. Use middleware to protect profile endpoints and allow users to update their information securely.

@app.post('/user', response_model=User)
async def registeration(last_name: Annotated[str, Form()], first_name: Annotated[str, Form()], username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()]):
    path =  "./user_profile/users.json"
    f = file_update.openfile(path)
    for key in f:
        if key != "counter":
            user = f.get(key).get("email")
            print(user)
            if key == username:
                return JSONResponse(content={"error": "User already exist"})
            if user == email:
                return JSONResponse(content={"error": "Email already used"})
    hash_password = to_do_auth.bcrypt.using(rounds=13).hash(password)
    
    if f.get("counter"):
        f["counter"] = f.get("counter") + 1
    else:
        f["counter"] = 1
    id = f["counter"]
    new_user = {
        "last_name":last_name,
        "first_name":first_name,
        "username":username,
        "password": hash_password,
        "email": email , 
        "id":  id   
    }
    f[username] = new_user
    f = file_update.updatefile(path, f)
    list = ["last_name", "first_name", "username", "id", "email"]
    serilized = file_update.serializer(list, new_user)
    return JSONResponse(content={"mesaage": "user created succesfully", "user_details": serilized})

@app.post("/user_login", response_model=User)
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    path ="./user_profile/users.json"
    f = file_update.openfile(path)
    for key in f:
        if key == username:
            user_details = f[username]
            check = to_do_auth.password_verification(password, user_details['password'])
            if check is True:
                token = to_do_auth.get_token(f[username])
                return JSONResponse(content={"message": "login successful", "bearer_token": token})
            else:
                return JSONResponse(content={"error_message": "incorrect username or password"})    
    return JSONResponse(content={"error_message": "incorrect username or password"})

@app.put("/user")
async def updateProfile(last_name:Annotated[str, Form()]= None, first_name: Annotated[str, Form()]= None):
    path ="./user_profile/users.json"
    f = file_update.openfile(path)
    if  to_do_auth.current_user:
        #user = f[to_do_auth.current_user]
        if first_name: 
            f[to_do_auth.current_user]["first_name"] = first_name
        if last_name:
            f[to_do_auth.current_user]["last_name"] =last_name
        file_update.updatefile(path, f)
        list = ["last_name", "first_name", "username", "id", "email"]
        serialized = file_update.serializer(list, f[to_do_auth.current_user])
        return JSONResponse(content={"updated": serialized})
    return JSONResponse(content={"error": "Unauthorised user"}) 
            
# OAuth2 Secured Notes API:
# Build a notes API with OAuth2 authentication. Use middleware to ensure that users can only access their own notes, providing a secure way to manage personal information.
@app.post("/note", response_model=Note)
async def createnote(title: Annotated[str, Form()], body: Annotated[str, Form()]):
    path =  "./notes/notes.json"
    f = file_update.openfile(path)
    f[0] = f[0] + 1
    user = to_do_auth.current_user
    new_note = {
        "id": f[0],
        "title": title,
        "body": body,
        "created_by": user        
    }
    f.append(new_note)
    file_update.updatefile(path, f)
    return JSONResponse(content={"note_craeted": new_note})
    
@app.get("/note", response_model=Note)
async def current_user_note():
    path =  "./notes/notes.json"
    notes = file_update.openfile(path)
    user_note = []
    for note in notes:
        if note != notes[0]:
            if note["created_by"] == to_do_auth.current_user:
                user_note.append(note)
    return JSONResponse(content={"list": user_note})
            
@app.get("/note/{id}", response_model=Note) 
async def get_one_note(id: Annotated[int, id]):
    path =  "./notes/notes.json"
    notes = file_update.openfile(path)
    for note in notes:
        if note != notes[0]:
            if note["created_by"] == to_do_auth.current_user:
                if note["id"] == id:                  
                    return JSONResponse(content={"list": note})
    return JSONResponse(content={"error": "note not found"})
    
# OAuth2 Protected Blog API:
# Create a blog API where users can log in with OAuth2 to create, edit, and delete blog posts. Use middleware to restrict actions to authenticated users only.
@app.post("/blog", response_model=Blog)
async def createblog(title: Annotated[str, Form()], body: Annotated[str, Form()]):
    path =  "./blogs/blogs.json"
    f = file_update.openfile(path)
    f[0] = f[0] + 1
    user = to_do_auth.current_user
    new_blog = {
        "id": f[0],
        "title": title,
        "body": body,
        "created_by": user,
        "is_published": False    
    }
    f.append(new_blog)
    file_update.updatefile(path, f)
    return JSONResponse(content={"blog_craeted": new_blog})
    
@app.get("/blog")
async def current_user_blog():
    path =  "./blogs/blogs.json"
    blogs = file_update.openfile(path)
    user_blog = []
    for blog in blogs:
        if blog != blogs[0]:
            if blog["created_by"] == to_do_auth.current_user:
                user_blog.append(blog)
                return JSONResponse(content={"list": user_blog})
    return JSONResponse(content={"message": "No blog post"})
            
@app.get("/blog/{id}") 
async def get_one_blog(id: Annotated[int, id]):
    path =  "./blogs/blogs.json"
    blogs = file_update.openfile(path)
    for blog in blogs:
        if blog != blogs[0]:
            if blog["created_by"] == to_do_auth.current_user:
                if blog["id"] == id:                  
                    return JSONResponse(content={"list": blog})
    return JSONResponse(content={"error": "blog not found"})

@app.put("/blog/{id}", response_model=Blog)
async def update_blog(id: Annotated[int, id], title: Annotated[str, Form()] = None, body: Annotated[str, Form()] =None, is_published: Annotated[bool, Form()] =None  ):
    path =  "./blogs/blogs.json"
    blogs = file_update.openfile(path)
    print(is_published)
    for blog in blogs:
        #print(blog)
        if blog != blogs[0]:
            
            if blog["created_by"] == to_do_auth.current_user:
                if blog["id"] == id: 
                    print(blog)
                    if title:
                        print(blog)
                        blog["title"] = title
                    if body:
                        print(blog)
                        blog["body"] = body
                    if is_published is not None:
                        print(blog)
                        blog["is_published"] = is_published
                        file_update.updatefile(path, blogs)
                        return JSONResponse(content={"updated_blog": blog})
    return JSONResponse(content={"error": "blog not found"})                 

@app.delete("/blog/{id}")
async def delete_blog():
    path =  "./blogs/blogs.json"
    blogs = file_update.openfile(path)
    for blog in blogs:
        if blog != blogs[0]:
            if blog["created_by"] == to_do_auth.current_user:
                if blog["id"] == id: 
                    blog.remove(blog)                 
                    return JSONResponse(content={"message": "blog post deleted"})
    return JSONResponse(content={"error": "blog not found"})

# OAuth2 E-commerce API:
# Develop an e-commerce API with OAuth2 for user authentication. Implement middleware to protect user actions like viewing order history, placing orders, and managing account details.

@app. get("/history")
async def history():
    path =  "./e-commerce/history.json"
    histories = file_update.openfile(path)
    for history in histories:
        if history != histories[0]:
            if history["userId"] == to_do_auth.current_user:
                return JSONResponse(content={"histroy": history})
                
    return JSONResponse(content={"message": "User has no purchase histroy"}) 