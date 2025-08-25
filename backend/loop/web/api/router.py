from fastapi.routing import APIRouter

from loop.web.api import echo, learning, monitoring, redis, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
