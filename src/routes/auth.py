from fastapi import APIRouter, Response
from service import AuthService
from dtypes import make_response, NewUserRequest
from util import DatabaseSession

auth_service = AuthService(
    dbc=DatabaseSession()
)

router = APIRouter(prefix="/api/v1/auth")

@router.post("/")
async def create_user(user: NewUserRequest, response: Response):
    print(user.__dict__)
    success, data = auth_service.register(**user.__dict__)
    return make_response(201 if success else 400, data=data)