from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT


from app.auth.api import router as auth_router
from app.users.api import router as users_router
from app.websocket.websocket import router as ws_router
from app.settings import Settings


SETTINGS = Settings()

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return SETTINGS


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(ws_router)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

