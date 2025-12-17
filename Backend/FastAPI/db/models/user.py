from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None  # <- In MongoDB the id is a string per default
    username: str
    email: str
    