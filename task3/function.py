import json

def load_file():
    with open("code_storage.json", "r") as f:
        code_collection = json.load(f)
        return code_collection
    
def update_file(update_code):
    with open("code_storage.json", "w") as f:
        json.dump(update_code, f)

def delete(code_collections, code_number, email):
    code_number = str(code_number)
    #print(code_collections)
    filtered_codes = [code for code in code_collections if code["code"] != code_number or code['email'] != email]
    #print(filtered_codes)
    return filtered_codes
        
def load_users():
    with open("user.json", "r") as f:
        users_collection = json.load(f)
        return users_collection
    
def update_user(update_user):
    with open("user.json", "w") as f:
        json.dump(update_user, f)
        
def activate_user(email, users):
    users = users
    for user in users:
        if user['email'] == email:
            user['isActivated'] = True
            break
    return users


