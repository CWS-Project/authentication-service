class AuthController:
    _db_client = None

    def __init__(self, dbc) -> None:
        self._db_client = dbc
    
    def login(self, email: str, password: str) -> list[bool, dict | None]:
        if email == "a" and password == "b":
            return True, {"token": "123"}
        return False, None