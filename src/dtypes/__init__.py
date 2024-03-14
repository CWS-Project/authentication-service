from .response import ApiResponse

def make_response(status:int, message:str = "", data:dict | list | None = None) -> ApiResponse:
    return ApiResponse(status=status, message=message, data=data)