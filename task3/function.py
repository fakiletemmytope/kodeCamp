import json

def load_file():
    with open("code_storage.json", "r") as f:
        code_collection = json.load(f)
        return code_collection
    
def update_file(update_code):
    with open("code_storage.json", "w") as f:
        json.dump(update_code, f)

def delete(code_collections, code_number, email):
    for code in code_collections:        
        if code["id"] == code_number and code['email'] == email:
            code_collections.remove(code)
            return code_collections