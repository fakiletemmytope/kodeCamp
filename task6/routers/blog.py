from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated
from database.models import Blog
from database.db_connect import Session
from sqlalchemy.exc import SQLAlchemyError
from utils.serializer import serialize
 



router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
    responses={404: {"description": "Not found"}},   
)

class BlogForm(BaseModel):
    title: str
    body: str

# Blog API:
# Create a blog API where users can create, read, update, and delete blog posts. Store posts, authors, and comments in an SQLite database.

# get all user's blog
@router.get("/")
async def all_blogs(request: Request):
    id = request.state.custom_data["current_userId"]
    try:        
        session = Session()
        result = session.query(Blog).where(Blog.author_id == id).all()
        print(result)
        param = ["title", "body", "author_name"]
        if result:  
            list = []
            for row in result:
                list.append(await serialize(param, row))     
            session.commit()
            session.close()
            return JSONResponse(content={
                "blogs": list
            },status_code=200)
        else:
            session.close()
            return JSONResponse(content={
                "messsage": "No blog found"
            },status_code=403)
    except SQLAlchemyError as e:
        session.close()
        return  JSONResponse(content={
            "message": e
        })
    except Exception as e:
        session.rollback()  # Rollback the transaction on any other errors
        return JSONResponse(
            content={
                "details": "An unexpected error occurred",
                "error": str(e)  # Provide the error details
            },
            status_code=500  # HTTP status code for server error
        )

# get one blog
@router.get("/{blog_id}")
async def blog(blog_id: int, request: Request):
    id = request.state.custom_data["current_userId"]
    try:        
        session = Session()
        result = session.query(Blog).where(Blog.author_id == id, Blog.id == blog_id).one()
        param = ["title", "body", "author_name"]
        if result:     
            serialized = await serialize(param, result)       
            return JSONResponse(content={
                "blog": serialized
            },status_code=200)
        else:
            session.close()
            return JSONResponse(content={
                "messsage": "No blog found"
            },status_code=403)
    except SQLAlchemyError as e:
        session.close()
        return  JSONResponse(content={
            "message": e
        })
    except Exception as e:
        session.rollback()  # Rollback the transaction on any other errors
        return JSONResponse(
            content={
                "details": "An unexpected error occurred",
                "error": str(e)  # Provide the error details
            },
            status_code=500  # HTTP status code for server error
        )

# post a blog
@router.post("/")
async def create(title: Annotated[str, Form()], body: Annotated[str, Form()], request: Request):
    
    user = request.state.custom_data
    blog = Blog(title=title, 
                    body=body, 
                    author_name= user["current_username"], 
                    author_id= user["current_userId"] )
    session = Session()
    try:               
        session.add(blog)
        session.commit()
        session.close()
        return JSONResponse(content={"message": "Blog created"},
                            status_code=201)
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
 
# update a blog   
@router.put("/{blog_id}")
async def update(request: Request, blog_id: int, title: Annotated[str, Form()] =None, body: Annotated[str, Form()] = None):
    id = request.state.custom_data["current_userId"]
    try:
        session = Session()
        result = session.query(Blog).filter(Blog.id == blog_id, Blog.author_id == id)
        if result:
            if title:
                result.update({Blog.title: title})
            if body:
                result.update({Blog.body: body})
            session.commit()
            session.close()
            return JSONResponse(content={"message": "Blog updated"})
        else:
            return JSONResponse(content={
                "message": "Blog not found"
            })
    except SQLAlchemyError as e:
        return JSONResponse(content={
                "message": str(e)
        })
    except Exception as e:
        return JSONResponse(content={
                "message": str(e)
        })
    
# delete a blog
@router.delete("/{blog_id}")
async def delete(request: Request, blog_id: int):
    id = request.state.custom_data["current_userId"]
    try:
        session = Session()
        result = session.query(Blog).filter(Blog.id == blog_id, Blog.author_id == id)
        if result:
            result.delete()
            session.commit()
            session.close()
            return JSONResponse(content={"message": "Blog deleted"}, status_code=210)
        else:
            return JSONResponse(content={
                "message": "Blog not found"
            }, status_code=403)
    except SQLAlchemyError as e:
        return JSONResponse(content={
                "message": str(e)
        }, status_code=500)
    except Exception as e:
        return JSONResponse(content={
                "message": str(e)
        }, status_code=500)
