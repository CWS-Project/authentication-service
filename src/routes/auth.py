from fastapi import APIRouter, Response
from controller import AuthController
from dtypes import make_response

auth_controller = AuthController("a")

router = APIRouter(prefix="/api/v1/auth")

@router.post("/")
async def login_user(response: Response):
    success, data = auth_controller.login("a", "b")
    if not success:
        response.status_code = 400
        return make_response(400, "Invalid credentials")
    return make_response(200, "OK", data)