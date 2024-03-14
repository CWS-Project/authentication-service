from fastapi import FastAPI
from dtypes import make_response
from routes import auth_router

app = FastAPI()
app.include_router(auth_router)

@app.get("/healthz")
def health_check():
    return make_response(200, "OK")