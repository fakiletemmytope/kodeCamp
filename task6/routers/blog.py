from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Annotated
from database.models import User, Blog
from database.db_connect import Session
from utils.authenticate import current_user



router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
    responses={404: {"description": "Not found"}},   
)

class Blog(BaseModel):
    title: str
    body: str

# Blog API:
# Create a blog API where users can create, read, update, and delete blog posts. Store posts, authors, and comments in an SQLite database.
@router.get("/")
async def all_blogs():
    user = current_user
    session = Session()
    session.query(Blog).where(Blog.author_id == current_user["id"])
    session.commit()
    session.close()
    
    
    return "all blogs"

@router.get("/{id}")
async def blog(id: Annotated[int, id]):
    return "one blog"

@router.post("/")
async def create(title: Annotated[str, Form()], body: Annotated[str, Form()]):
    print(type(current_user))
    # session = Session()c
    # blog = Blog(title=title, 
    #             body=body, 
    #             author_name=user["username"], 
    #             author_id= user["id"] )
    # session.add(blog)
    # session.commit()
    # session.close()
    return "create blog"

@router.put("/{id}")
async def update():
    return "update bog"

@router.delete("/{id}")
async def delete():
    return "create blog"