from fastapi import Header
from ..database import UserManager
from ..exceptions import BaseException

async def auth(authorization: str = Header()) -> None:
    """Authentication dependency (executes before the route handler)"""
    
    key = authorization.replace("Bearer ", "", 1)
    
    print(f"[!] Incoming request key: {key}")

    if not key:
        raise BaseException("Missing authorization header.", status=401, type="authentication_error")
    
    if not await UserManager.check_key(key):
        raise BaseException("Your key is invalid.", status=401, type="authentication_error")
    
    if await UserManager.get_property(key, "banned"):
        raise BaseException("Your key is banned.", status=403, type="forbidden_error")