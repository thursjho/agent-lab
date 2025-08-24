from litestar import Litestar, get
from typing import Dict

from .controllers.chat_controller import ChatController
from .dependencies import dependencies


@get("/")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "chat-api"}


app = Litestar(
    route_handlers=[health_check, ChatController],
    dependencies=dependencies
)