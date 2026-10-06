import redis

from app.core.config import settings

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)


def _key(jti: str) -> str:
    return f"refresh_token:{jti}"


def store_refresh_token(jti: str, user_id: int):
    r.set(_key(jti), user_id, ex=settings.refresh_token_expire_minutes * 60)


def is_refresh_token_active(jti: str) -> bool:
    return r.exists(_key(jti)) == 1


def revoke_refresh_token(jti: str) -> None:
    r.delete(_key(jti))
