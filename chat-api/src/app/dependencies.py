"""
Dependency Injection 설정
Litestar DI를 사용한 의존성 주입 구성
"""

import logging
from litestar.di import Provide

from ..agents import DefaultAgent
from .services.chat_service import ChatService

logger = logging.getLogger(__name__)


def get_default_agent() -> DefaultAgent:
    """DefaultAgent 팩토리 함수"""
    try:
        agent = DefaultAgent()
        logger.info(f"DefaultAgent 생성: {agent.name} v{agent.version}")
        return agent
    except Exception as e:
        logger.error(f"DefaultAgent 생성 실패: {e}")
        raise


def get_chat_service(agent: DefaultAgent) -> ChatService:
    """ChatService 팩토리 함수"""
    return ChatService(agent)


# 의존성 주입 설정
dependencies = {
    "default_agent": Provide(get_default_agent, scope="singleton"),
    "chat_service": Provide(get_chat_service, scope="singleton")
}