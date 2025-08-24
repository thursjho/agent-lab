"""
Chat Application Service
채팅 관련 비즈니스 로직 처리
"""

import logging
from typing import List, Optional, AsyncGenerator
from dataclasses import dataclass

from ...agents import BaseAgent, ChatMessage

logger = logging.getLogger(__name__)


@dataclass
class ChatRequest:
    """채팅 요청 도메인 모델"""
    message: str
    history: Optional[List[ChatMessage]] = None


@dataclass 
class ChatResponse:
    """채팅 응답 도메인 모델"""
    message: str
    model: str
    agent_name: str
    agent_version: str


class ChatService:
    """채팅 애플리케이션 서비스"""
    
    def __init__(self, agent: BaseAgent):
        """
        Args:
            agent: 주입받을 에이전트 인스턴스
        """
        self._agent = agent
        logger.info(f"ChatService 초기화: {agent.name} v{agent.version}")
    
    async def send_message(self, request: ChatRequest) -> ChatResponse:
        """
        메시지 전송 및 응답 생성
        
        Args:
            request: 채팅 요청
            
        Returns:
            채팅 응답
            
        Raises:
            ValueError: 처리 실패
        """
        try:
            # 에이전트 호출
            response_message = await self._agent.invoke(
                message=request.message,
                chat_history=request.history
            )
            
            return ChatResponse(
                message=response_message,
                model=self._agent.config.model,
                agent_name=self._agent.name,
                agent_version=self._agent.version
            )
            
        except Exception as e:
            logger.error(f"메시지 처리 중 오류: {e}", exc_info=True)
            raise ValueError(f"메시지 처리 실패: {str(e)}")
    
    async def stream_message(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        """
        스트리밍 메시지 전송
        
        Args:
            request: 채팅 요청
            
        Yields:
            응답 청크들
            
        Raises:
            ValueError: 처리 실패
        """
        try:
            async for chunk in self._agent.stream(
                message=request.message,
                chat_history=request.history
            ):
                if chunk:
                    yield chunk
                    
        except Exception as e:
            logger.error(f"스트림 처리 중 오류: {e}", exc_info=True)
            raise ValueError(f"스트림 처리 실패: {str(e)}")
    
    async def health_check(self) -> dict:
        """
        서비스 상태 확인
        
        Returns:
            상태 정보
        """
        try:
            agent_health = await self._agent.health_check()
            
            return {
                "status": "healthy",
                "model": self._agent.config.model,
                "agent": self._agent.name,
                "version": self._agent.version,
                "details": agent_health
            }
            
        except Exception as e:
            logger.error(f"헬스 체크 중 오류: {e}")
            return {
                "status": "unhealthy",
                "model": "unknown",
                "agent": "unknown", 
                "version": "unknown",
                "error": str(e)
            }