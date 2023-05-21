from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_jwt_auth import AuthJWT


class FastapiJwtAuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(FastapiJwtAuthBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            FastapiJwtAuthBearer, self
        ).__call__(request)
        if credentials:
            auth = AuthJWT(req=request)
            auth.jwt_required()
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
