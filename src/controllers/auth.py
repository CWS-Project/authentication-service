from fastapi import APIRouter, Response, Request
from service import AuthService
from dtypes import make_response, NewUserRequest
from util import DatabaseSession, JWTHandler
import base64

auth_service = AuthService(
    dbc=DatabaseSession(),
    jwth=JWTHandler()
)

router = APIRouter(prefix="/api/v1/auth")

@router.post("/")
async def create_user(user: NewUserRequest, response: Response):
    success, data = auth_service.register(**user.__dict__)
    response.status_code = 201 if success else 400
    return make_response(201 if success else 400, data=data)

@router.get("/token")
async def login(request: Request, response: Response):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return make_response(400, message="Authorization header not found")
    
    auth_type, auth_token = auth_header.split(" ")
    if auth_type.lower() != "basic":
        return make_response(400, message="Invalid authorization type")
    
    if not auth_token:
        return make_response(400, message="Authorization token not found")
    
    username, password = base64.b64decode(auth_token).decode("utf-8").split(":")
    success, data = auth_service.login(username, password)
    response.status_code = 200 if success else 400
    return make_response(200 if success else 400, data=data)

@router.get("/me")
async def my_profile(request: Request, response: Response):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return make_response(400, message="Authorization header not found")
    
    auth_type, auth_token = auth_header.split(" ")
    if auth_type.lower() != "bearer":
        return make_response(400, message="Invalid authorization type")
    
    if not auth_token:
        return make_response(400, message="Authorization token not found")
    
    success, data = auth_service.get_current_user(auth_token)
    response.status_code = 200 if success else 400
    return make_response(200 if success else 400, data=data)

@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return make_response(400, message="Authorization header not found")
    
    auth_type, auth_token = auth_header.split(" ")
    if auth_type.lower() != "bearer":
        return make_response(400, message="Invalid authorization type")
    
    if not auth_token:
        return make_response(400, message="Authorization token not found")
    
    body = await request.json()
    if not body:
        return make_response(400, message="Request body not found")
    
    refresh_tok = body.get("refresh_token")
    if not refresh_tok:
        return make_response(400, message="Refresh token not found")
    
    success, data = auth_service.refresh_session(auth_token, refresh_tok)
    response.status_code = 200 if success else 400
    return make_response(
        200 if success else 400, 
        message="Refresh Success" if success else "Refresh failed", 
        data=data
    )
