from fastapi.routing import APIRouter

from loop.web.api import learning, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(learning.router, prefix="/learning", tags=["learning"])
