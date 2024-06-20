import os
import hashlib
from datetime import datetime, timedelta, timezone
from fastapi import Request
from redis.asyncio import Redis
from ..database import UserManager
from ..exceptions import InvalidRequestException

redis = Redis.from_url(os.environ["REDIS_URI"])

rate_limits = {
    "default": 3,
    "premium": 15
}

async def rate_limit(request: Request) -> None:
    """Rate limiting dependency (executes before the route handler)"""

    user = request.headers.get("Authorization", "").replace("Bearer ", "", 1)
    is_premium = await UserManager.get_property(user, "premium")

    username_hash = hashlib.sha256(bytes(user, "utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{username_hash}_{current_minute}"
    current_count = await redis.incr(redis_key)

    if current_count == 1:
        await redis.expireat(name=redis_key, when=now + timedelta(minutes=1))

    if current_count > rate_limits["premium" if is_premium else "default"]:
        raise InvalidRequestException("Rate limit exceeded.", status=429)