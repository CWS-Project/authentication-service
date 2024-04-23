from fastapi import APIRouter, Response, Request
from service import CustomerService
from util import DatabaseSession
from dtypes import (
    AddToCartRequest,
    RemoveFromCartRequest, 
    AddToWishlistRequest, 
    RemoveFromWishlistRequest, 
    make_response
)

customer_service = CustomerService(
    dbc=DatabaseSession()
)

router = APIRouter(prefix="/api/v1/customer")

@router.get("/cart/{user_id}")
async def get_cart(user_id: str, response: Response):
    print(user_id)
    success, result = customer_service.get_cart_by_user(user_id)
    if not success:
        return make_response(response, 400, message="Failed to get cart")
    return make_response(response, data=result, message="Cart retrieved successfully")

@router.post("/cart/{user_id}")
async def add_to_cart(user_id: str, request: AddToCartRequest, response: Response):
    success, result = customer_service.add_to_cart(user_id, request.product_id, request.quantity)
    if not success:
        return make_response(response, 400, message="Failed to add to cart")
    return make_response(response, data=result, message="Added to cart successfully")

@router.delete("/cart/{user_id}")
async def remove_from_cart(user_id: str, request: RemoveFromCartRequest, response: Response):
    success, result = customer_service.remove_from_cart(user_id, request.product_id)
    if not success:
        return make_response(response, 400, message="Failed to remove from cart")
    return make_response(response, data=result, message="Removed from cart successfully")

@router.get("/wishlist/{user_id}")
async def get_wishlist(user_id: str, response: Response):
    success, result = customer_service.get_wishlist_by_user(user_id)
    if not success:
        return make_response(response, 400, message="Failed to get wishlist")
    return make_response(response, data=result, message="Wishlist retrieved successfully")

@router.post("/wishlist/{user_id}")
async def add_to_wishlist(user_id: str, request: AddToWishlistRequest, response: Response):
    success, result = customer_service.add_to_wishlist(user_id, request.product_id)
    if not success:
        return make_response(response, 400, message="Failed to add to wishlist")
    return make_response(response, data=result, message="Added to wishlist successfully")

@router.delete("/wishlist/{user_id}")
async def remove_from_wishlist(user_id: str, request: RemoveFromWishlistRequest, response: Response):
    success, result = customer_service.remove_from_wishlist(user_id, request.product_id)
    if not success:
        return make_response(response, 400, message="Failed to remove from wishlist")
    return make_response(response, data=result, message="Removed from wishlist successfully")

@router.get("/address/{user_id}")
async def get_address(user_id: str, response: Response):
    success, result = customer_service.get_address(user_id)
    if not success:
        return make_response(response, 400, message="Failed to get address")
    return make_response(response, data=result, message="Address retrieved successfully")

@router.get("/profile/{user_id}")
async def get_profile(user_id: str, response: Response):
    success, result = customer_service.get_profile(user_id)
    if not success:
        return make_response(response, 400, message="Failed to get profile")
    return make_response(response, data=result, message="Profile retrieved successfully")