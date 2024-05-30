import json

def load_file():
    with open("books.json", "r") as f:
        book_collection = json.load(f)
        return book_collection
    
def update_file(updated_book):
    with open("books.json", "w") as f:
        json.dump(updated_book, f)

def delete_book(book_collections, id):
    for book in book_collections:        
        if book["id"] == id:
            book_collections.remove(book)
            return book_collections