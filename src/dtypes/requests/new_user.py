from pydantic import BaseModel
from datetime import datetime
from typing import List

class Address(BaseModel):
    line1: str
    line2: str | None = None
    city: str
    district: str
    state: str
    postal_code: str
    country: str

class Cart(BaseModel):
    product_id: str
    quantity: int

class Wishlist(BaseModel):
    product_id: str

class NewUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    address: Address
    cart: List[Cart] = []
    wishlist: List[Wishlist] = []
    is_active: bool = True
    is_admin: bool = False
    is_verified: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()