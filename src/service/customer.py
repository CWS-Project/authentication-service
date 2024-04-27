from util import DatabaseSession
from typing import Tuple
from bson.objectid import ObjectId

class CustomerService:
    _db_client: DatabaseSession

    def __init__(self, dbc: DatabaseSession) -> None:
        self._db_client = dbc
    
    def get_cart_by_user(self, user_id: str) -> Tuple[bool, dict | None]:
        success, cart = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"cart": 1})
        if not success:
            return False, None
        return True, cart["cart"]
    
    def add_to_cart(self, user_id: str, product_id: str, quantity: int) -> Tuple[bool, dict]:
        success, cart = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"cart": 1})
        if not success:
            return False, None
        # Check if product already exists in cart
        for item in cart["cart"]:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                success, _ = self._db_client.updateOne("users", {"_id": ObjectId(user_id)}, {"cart": cart["cart"]})
                return success, cart["cart"]
        cart["cart"].append({"product_id": product_id, "quantity": quantity})
        success, _ = self._db_client.updateOne("users", {"_id": ObjectId(user_id)}, {"cart": cart["cart"]})
        return success, cart["cart"]
    
    def remove_from_cart(self, user_id: str, product_id: str) -> Tuple[bool, dict]:
        success, cart = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"_id": 0, "password": 0})
        if not success:
            return False, None
        cart["cart"] = [item for item in cart["cart"] if item["product_id"] != product_id]
        success, _ = self._db_client.updateOne("users", {"_id": ObjectId(user_id)}, {"cart": cart["cart"]})
        return success, cart["cart"]
    
    def get_wishlist_by_user(self, user_id: str) -> Tuple[bool, dict | None]:
        success, wishlist = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"_id": 0, "password": 0})
        if not success:
            return False, None
        return True, wishlist["wishlist"]
    
    def add_to_wishlist(self, user_id: str, product_id: str) -> Tuple[bool, dict]:
        success, wishlist = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"_id": 0, "password": 0})
        if not success:
            return False, None
        wishlist["wishlist"].append({"product_id": product_id})
        success, _ = self._db_client.updateOne("users", {"_id": ObjectId(user_id)}, {"wishlist": wishlist["wishlist"]})
        return success, wishlist["wishlist"]
    
    def remove_from_wishlist(self, user_id: str, product_id: str) -> Tuple[bool, dict]:
        success, wishlist = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"_id": 0, "password": 0})
        if not success:
            return False, None
        wishlist["wishlist"] = [item for item in wishlist["wishlist"] if item["product_id"] != product_id]
        success, _ = self._db_client.updateOne("users", {"_id": ObjectId(user_id)}, {"wishlist": wishlist["wishlist"]})
        return success, wishlist["wishlist"]
    
    def get_address(self, user_id: str) -> Tuple[bool, dict]:
        success, address = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"_id": 0, "password": 0})
        if not success:
            return False, None
        return True, address["address"]
    
    def get_profile(self, user_id: str) -> Tuple[bool, dict]:
        success, profile = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, {"_id": 0, "password": 0})
        if not success:
            return False, None
        return True, profile
    
