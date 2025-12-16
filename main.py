from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#ROUTES
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return "Hola FastAPI!"


@app.get("/url")
async def url():
    return {"url": "https://mouredev.com/python"}

# Url local: http://localhost:8000/
# Activate enviorement (Windows): .venv\Scripts\activate
# Run server: uvicorn main:app --reload