from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Inicializar el server -> uvicorn users:router --reload
router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"message": "Not found"}})

# Entididad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id=1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
    User(id=2, name="Moure", surname="Dev", url="https://mouredev.com", age=35),
    User(id=3, name="Brais", surname="Dahlberg", url="https://haakon.com", age=33)
]

@router.get("/usersjson")
async def usersjson():
    return [{"name" : "Juan", "surname" : "Perez", "url" : "https://juanperez.com", "age" : 30},
            {"name" : "Ana", "surname" : "Gomez", "url" : "https://anagomez.com", "age" : 25},
            {"name" : "Luis", "surname" : "Martinez", "url" : "https://luismartinez.com", "age" : 28}]

@router.get("/users")
async def users():
    return users_list

@router.get("/user/{id}") #Path
async def user(id: int):
    return search_user(id)

@router.get("/user/") #Query
async def user(id: int):
    return search_user(id)

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}
# POST
@router.post("/user/", response_model=User ,status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        users_list.routerend(user)
    
# PUT
@router.put("/user/")
async def update_user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "User not found"}
    return user

# DELETE
@router.delete("/user/{id}")
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "User not found"}