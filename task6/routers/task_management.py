# Task Management API:
# Create a task management API where users can create, update, delete, and retrieve tasks. Use SQLite to store tasks, users, and task statuses
from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated
from database.models import Task
from database.db_connect import Session
from sqlalchemy.exc import SQLAlchemyError
from utils.serializer import serialize
 

router = APIRouter(
    prefix="/task",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},   
)

class TaskForm(BaseModel):
    title: str
    description: str
    is_published: bool = False
    
# get all user's blog
@router.get("/")
async def all_tasks(request: Request):
    id = request.state.custom_data["current_userId"]
    try:        
        session = Session()
        result = session.query(Task).where(Task.author_id == id).all()
        print(result)
        param = ["title", "description", "author_name"]
        if result:  
            list = []
            for row in result:
                list.append(await serialize(param, row))     
            session.commit()
            session.close()
            return JSONResponse(content={
                "tasks": list
            },status_code=200)
        else:
            session.close()
            return JSONResponse(content={
                "messsage": "No Task found"
            },status_code=403)
    except SQLAlchemyError as e:
        session.close()
        return  JSONResponse(content={
            "message": str(e)
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


@router.get("/{task_id}")
async def task(task_id: int, request: Request):
    id = request.state.custom_data["current_userId"]
    try:        
        session = Session()
        result = session.query(Task).where(Task.author_id == id, Task.id == task_id).one()
        param = ["title", "description", "author_name"]
        if result:     
            serialized = await serialize(param, result)       
            return JSONResponse(content={
                "task": serialized
            },status_code=200)
        else:
            session.close()
            return JSONResponse(content={
                "messsage": "No task found"
            },status_code=403)
    except SQLAlchemyError as e:
        session.close()
        return  JSONResponse(content={
            "message": str(e)
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

# post a task
@router.post("/")
async def create(title: Annotated[str, Form()], description: Annotated[str, Form()], request: Request, is_published: Annotated[bool, Form()]= False):
    user = request.state.custom_data
    task = Task(title=title, 
                    description=description, 
                    author_name= user["current_username"], 
                    author_id= user["current_userId"] )
    session = Session()
    try:               
        session.add(task)
        session.commit()
        session.close()
        return JSONResponse(content={"message": "Task created"},
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
 
# update a task   
@router.put("/{task_id}")
async def update(request: Request, task_id: int, title: Annotated[str, Form()] =None, description: Annotated[str, Form()] = None, is_published: Annotated[bool, Form()] = None):
    id = request.state.custom_data["current_userId"]
    try:
        session = Session()
        result = session.query(Task).filter(Task.id == task_id, Task.author_id == id)
        if result:
            if title:
                result.update({Task.title: title})
            if description:
                result.update({Task.description: description})
            if is_published:
                result.update({Task.is_published: is_published})
            session.commit()
            session.close()
            return JSONResponse(content={"message": "Task updated"})
        else:
            return JSONResponse(content={
                "message": "Task not found"
            })
    except SQLAlchemyError as e:
        return JSONResponse(content={
                "message": str(e)
        })
    except Exception as e:
        return JSONResponse(content={
                "message": str(e)
        })
    
# delete a task
@router.delete("/{task_id}")
async def delete(request: Request, task_id: int):
    id = request.state.custom_data["current_userId"]
    try:
        session = Session()
        result = session.query(Task).filter(Task.id == task_id, Task.author_id == id)
        if result:
            result.delete()
            session.commit()
            session.close()
            return JSONResponse(content={"message": "Task deleted"}, status_code=210)
        else:
            return JSONResponse(content={
                "message": "Task not found"
            }, status_code=403)
    except SQLAlchemyError as e:
        return JSONResponse(content={
                "message": str(e)
        }, status_code=500)
    except Exception as e:
        return JSONResponse(content={
                "message": str(e)
        }, status_code=500)
