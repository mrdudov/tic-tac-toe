from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import IntegrityError

from app.auth.api import router as auth_router
from app.users.api import router as users_router
from app.websocket.websocket import router as ws_router
from app.settings import SETTINGS


app = FastAPI(root_path="/api/v1")


@AuthJWT.load_config
def get_config():
    return SETTINGS


app.include_router(auth_router)
app.include_router(users_router)
#app.include_router(ws_router)


@app.websocket("/api/v1/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@app.exception_handler(IntegrityError)
def sqlalchemy_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
