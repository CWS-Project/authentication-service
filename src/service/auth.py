from util import DatabaseSession
from typing import Tuple
import bcrypt

class AuthService:
    _db_client: DatabaseSession

    def __init__(self, dbc: DatabaseSession) -> None:
        self._db_client = dbc
    
    def login(self, email: str, password: str) -> list[bool, dict | None]:
        user = self._db_client.findOne("users", {"email": email})
        if not user:
            return False, None
        
        return False, None
    
    def register(self, **kwargs) -> Tuple[bool, dict]:
        success, user_id = self._db_client.insert("users", kwargs)
        return success, {"user_id": user_id}
    
    def get_profile_by_id(self, user_id: str) -> Tuple[bool, dict | None]:
        user = self._db_client.findOne("users", {"_id": user_id}, {"password": 0})
        if not user:
            return False, None
        return True, user