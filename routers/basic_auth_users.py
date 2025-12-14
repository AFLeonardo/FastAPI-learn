from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User): # Entidad que representa al usuario en la base de datos
    password: str

users_db = {
    "Valeria": {
        "username": "Valeria",
        "full_name": "Valeria Gomez",
        "email": "valeriag@gmail.com",
        "disable": False,
        "password": "valeria123" # <- In a real app, passwords should be hashed
    },
    "Carlos": {
        "username": "Carlos",
        "full_name": "Carlos Sanchez",
        "email": "carlos@hotmail.com",
        "disable": True,
        "password": "carlos456"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"} )
    
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    user = search_user_db(form.username)
    
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect password") 
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user