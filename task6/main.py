from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from routers import blog, user, task_management
from utils import authenticate




app = FastAPI() 

#middleware
@app.middleware("http")
async def authenticateUser(request: Request, call_next):
    urlpath = request.url.path
    verb = request.method
    #print(verb, urlpath)
    if urlpath == "/login" or urlpath == "/docs" or urlpath=="/" or urlpath=="/ecommerce/login":
        response = await call_next(request)
        return response
    elif urlpath == "/user" and verb == "POST":
        response = await call_next(request)
        return response
    elif urlpath == "ecommerce/order" and verb == "POST":
        response = await call_next(request)
        return response
    elif urlpath == "ecommerce/customer" and verb == "POST":
        response = await call_next(request)
        return response
    else:
        if request.headers.get("authorization"):
            decode = await authenticate.authenticate_token(request.headers.get("authorization").split(" ")[1])
            print(decode)
            if  decode is None:
                return JSONResponse(content={"detail":"Expired Token"}) 
            else:   
                current_username = decode["username"]   
                current_userId = decode["id"]  
                request.state.custom_data = {"current_username": current_username,
                                             "current_userId": current_userId} 
                response = await call_next(request)
                return response
        else:
            return JSONResponse(content={"detail":"Token required"}) 
        
#routes
app.include_router(user.router)
app.include_router(blog.router)
app.include_router(task_management.router)

#default route
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}




 



 

