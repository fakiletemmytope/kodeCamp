from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
import jwt

# auth = OAuth2PasswordBearer(url="todo_login")


def password_verification(password, hash):
    check = bcrypt.verify(password, hash)
    return check

SECRET_KEY = "e434573e0c4a5f0ebb67d41df3a2b400ae315b38ef74279614e33403dd17a04a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_token(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

current_user = "jjj"
def authenticate_token(token):
    decode = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    global current_user
    current_user= decode["username"]
    #print(current_user)
    #print(f'this: {decode}')
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
