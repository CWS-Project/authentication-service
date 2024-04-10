from pydantic import BaseModel

class AddToWishlistRequest(BaseModel):
    product_id: str