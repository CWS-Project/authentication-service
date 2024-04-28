from util import DatabaseSession, JWTHandler
from typing import Tuple
from bson.objectid import ObjectId
import bcrypt

class AuthService:
    _db_client: DatabaseSession
    _jwt_handler: JWTHandler

    def __init__(self, dbc: DatabaseSession, jwth: JWTHandler) -> None:
        self._db_client = dbc
        self._jwt_handler = jwth

    def login(self, email: str, password: str) -> Tuple[bool, dict | None]:
        success, user = self._db_client.findOne("users", {"email": email})
        if not user:
            return False, None
        if bcrypt.checkpw(password.encode("utf-8"), str(user["password"]).encode("utf-8")):
            access_token, refresh_token = self._jwt_handler.create_tokens({"user_id": str(user["_id"])})
            return True, {"access_token": access_token, "refresh_token": refresh_token}
        return False, None

    def register(self, **kwargs) -> Tuple[bool, dict]:
        kwargs["address"] = kwargs["address"].__dict__
        kwargs["password"] = bcrypt.hashpw(kwargs["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        success, user_id = self._db_client.insert("users", kwargs)
        return success, {"user_id": user_id}

    def get_profile_by_id(self, user_id: str) -> Tuple[bool, dict | None]:
        success, user = self._db_client.findOne("users", {"_id": ObjectId(user_id)}, col_excl={"password": 0})
        if not success:
            return False, None
        return True, user
    
    def get_current_user(self, access_token: str) -> Tuple[bool, dict | None]:
        data, _ = self._jwt_handler.verify_token(access_token)
        user_id = data.get("user_id")
        if not user_id:
            return False, None
        success, data = self.get_profile_by_id(user_id)
        data["_id"] = str(data["_id"])
        if not success:
            return False, None
        return True, data
    
    def refresh_session(self, access_token: str, refresh_token: str) -> Tuple[bool, dict | None]:
        data, error = self._jwt_handler.verify_token(refresh_token, True)
        if error:
            print(f"Auth Error: {error}")
            return False, None
        user_id = data.get("user_id")
        if not user_id:
            return False, None
        access_token, refresh_token = self._jwt_handler.create_tokens({"user_id": user_id})
        return True, {"access_token": access_token, "refresh_token": refresh_token}

    def change_password(self, access_token: str, current_password: str, new_password: str) -> Tuple[bool, dict | None]:
        data, error = self._jwt_handler.verify_token(access_token)
        if error:
            print(f"Auth Error: {error}")
            return False, None
        user_id = data.get("user_id")
        if not user_id:
            print("User ID not found")
            return False, None
        success, user = self._db_client.findOne("users", {"_id": ObjectId(user_id)})
        if not success:
            print("User not found")
            return False, None
        if bcrypt.checkpw(current_password.encode("utf-8"), str(user["password"]).encode("utf-8")):
            new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            success, _ = self._db_client.update("users", {"_id": ObjectId(user_id)}, {"password": new_password})
            return success, None
        print("Password mismatch")
        return False, None
