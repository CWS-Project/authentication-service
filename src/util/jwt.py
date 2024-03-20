import jwt, os
from datetime import datetime, timedelta
from typing import Tuple

class JWTHandler:
    secret: str
    algorithm: str
    access_token_expiration: int
    refresh_token_expiration: int
    issuer: str

    def __init__(
            self, 
            secret: str = os.getenv("JWT_SECRET"), 
            algorithm: str = "HS256", 
            access_token_expiration: int = 3600, 
            refresh_token_expiration: int = 86400, 
            issuer: str = "auth.simplestore.local"
        ) -> None:
        self.secret = secret
        self.algorithm = algorithm
        self.access_token_expiration = access_token_expiration
        self.refresh_token_expiration = refresh_token_expiration
        self.issuer = issuer
    
    @staticmethod
    def get_expiration_time(expiration: int):
        expire_date = datetime.now() + timedelta(seconds=expiration)
        return int(round(expire_date.timestamp()))
    
    def create_tokens(self, payload: dict):
        access_token_payload = {
            **payload,
            "exp": self.get_expiration_time(self.access_token_expiration),
            "iss": self.issuer,
            "iat": int(round(datetime.now().timestamp())),
            "nbf": int(round(datetime.now().timestamp()) - 1),
        }
        
        refresh_token_payload = {
            **payload,
            "exp": self.get_expiration_time(self.refresh_token_expiration),
            "iss": self.issuer,
            "iat": int(round(datetime.now().timestamp())),
            "nbf": int(round(datetime.now().timestamp()) - 1),
        }
        
        access_token = jwt.encode(access_token_payload, self.secret, algorithm=self.algorithm)
        refresh_token = jwt.encode(refresh_token_payload, self.secret, algorithm=self.algorithm)
        
        return access_token, refresh_token
    
    def verify_token(self, token: str, for_refresh: bool = False) -> Tuple[dict | None, str | None]:
        try:
            return jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                options={
                    'verify_exp': not for_refresh,
                    'verify_iss': True,
                    'verify_iat': True,
                    'verify_nbf': True,
                    'verify_signature': True,
                }
            ), None
        except jwt.ExpiredSignatureError:
            return None, "Token has expired"
    
    def refresh_tokens(self, access_token: str, refresh_token: str):
        rt_payload, error = self.verify_token(refresh_token)
        at_payload, error = self.verify_token(access_token, for_refresh=True)
        if error:
            return None, error
        if at_payload["id"] != rt_payload["id"]:
            return None, "Invalid token"
        return self.create_tokens(at_payload)