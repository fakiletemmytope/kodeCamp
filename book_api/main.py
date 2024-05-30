from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import json
from functions import load_file, update_file, delete_book

app = FastAPI()

 
class book(BaseModel):
    title: str
    author: str
    publication_year: str
    genre:str

@app.get("/")
def all_book():
    book_collections = load_file()
    length = len(book_collections)
    if length == 0:
        return {"message": "No book in the database"}
    return {"data" : book_collections}


@app.get("/{book_id}")
def one_book(book_id: int):
    book_collections = load_file()
    for book in book_collections:
        #print(book)
        if book["id"] == book_id:
            return {"book_details": book}
    return {"message" : "book does not exist"}


@app.post("/")
def create_book(book: book):
    book_collections = load_file()
    id =  len(book_collections)
    id = id + 1
    update_book = dict(book, id=id)
    book_collections.append(update_book)
    update_file(book_collections)
    return update_book
     

@app.put("/{book_id}")
def update_book(book_id: int, update_book: book):
    book_collections = load_file()
    for book in book_collections:        
        #print(book)
        if book["id"] == book_id:
            new_book = update_book.__dict__
            if new_book["title"]:
                book['title'] = new_book['title']
            if new_book["genre"]:
                book['genre'] = new_book['genre']
            if new_book["author"]:
                book['author'] = new_book['author']
            if new_book["publication_year"]:
                book['publication_year'] = new_book['publication_year']
            update_file(book_collections)       
            return {"book_details": book}
    
    return {"message" : "book does not exist"}


@app.delete("/{book_id}")
def delete_book(book_id: int):
    book_collections = load_file()
    #print(book_collections)
    for book in book_collections:        
        if book["id"] == book_id:
            book_collections.remove(book)
            update_file(book_collections)
            return {"message": "Deleted successfully"}
    return {"message" : "book does not exist"}
            
    
