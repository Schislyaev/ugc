# import jwt
from api.core.config import settings
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# def decode_jwt(token: str) -> dict:
#     try:
#         decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         return decoded_token if decoded_token["expires"] >= time.time() else None
#     except:
#         return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt():   # credentials.credentials
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self) -> bool:   # , jwtoken: str
        if settings.log_level == 'DEBUG':
            return True
        #
        # is_token_valid: bool = False
        #
        # try:
        #     payload = decode_jwt(jwtoken)
        # except Exception:
        #     payload = None
        # if payload:
        #     is_token_valid = True
        # return is_token_valid
