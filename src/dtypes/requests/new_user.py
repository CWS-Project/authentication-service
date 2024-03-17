from pydantic import BaseModel
from datetime import datetime

class NewUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    address1: str
    address2: str | None = None
    city: str
    state: str
    postal_code: str
    country: str
    is_active: bool = True
    is_admin: bool = False
    is_verified: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()