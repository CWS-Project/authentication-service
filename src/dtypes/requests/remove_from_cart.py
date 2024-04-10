from pydantic import BaseModel

class RemoveFromCartRequest(BaseModel):
    product_id: str