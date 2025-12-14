from fastapi import APIRouter

router = APIRouter(prefix="/products",
                    tags=["products"],
                   responses={404: {"message": "Not found"}})
products_list = [
    {"name": "Laptop", "price": 1200},
    {"name": "Smartphone", "price": 800},
    {"name": "Tablet", "price": 400}
]

@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]