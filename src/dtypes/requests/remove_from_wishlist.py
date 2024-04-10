from pydantic import BaseModel

class RemoveFromWishlistRequest(BaseModel):
    product_id: str