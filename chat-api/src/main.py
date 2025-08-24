from litestar import Litestar, get
from typing import Dict


@get("/")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "chat-api"}


@get("/api/health")
async def api_health() -> Dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}


app = Litestar(route_handlers=[health_check, api_health])