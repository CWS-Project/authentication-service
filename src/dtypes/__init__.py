from .response import ApiResponse
from .requests import NewUserRequest

def make_response(status:int, message:str = "", data:dict | list | None = None) -> ApiResponse:
    return ApiResponse(status=status, message=message, data=data)