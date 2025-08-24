"""
Base Agent 추상 클래스
모든 에이전트가 구현해야 하는 공통 인터페이스 정의
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """채팅 메시지 표준 형식"""
    role: str = Field(..., description="메시지 역할: user, assistant, system")
    content: str = Field(..., description="메시지 내용")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="추가 메타데이터")
    
    class Config:
        frozen = True  # immutable


class AgentConfig(BaseModel):
    """에이전트 설정"""
    name: str = Field(..., description="에이전트 이름")
    description: str = Field(..., description="에이전트 설명")
    version: str = Field(default="1.0.0", description="에이전트 버전")
    model: Optional[str] = Field(default=None, description="사용할 LLM 모델")
    temperature: Optional[float] = Field(default=None, description="모델 온도 설정")
    max_tokens: Optional[int] = Field(default=None, description="최대 토큰 수")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="추가 설정")


class BaseAgent(ABC):
    """모든 에이전트가 상속해야 하는 추상 기본 클래스"""
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Args:
            config: 에이전트 설정
        """
        self.config = config or AgentConfig(
            name=self.__class__.__name__,
            description=f"{self.__class__.__name__} agent"
        )
    
    @property
    @abstractmethod
    def name(self) -> str:
        """에이전트 이름 반환"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """에이전트 설명 반환"""
        pass
    
    @property
    def version(self) -> str:
        """에이전트 버전 반환"""
        return self.config.version
    
    @abstractmethod
    async def invoke(
        self, 
        message: str, 
        chat_history: Optional[List[ChatMessage]] = None,
        **kwargs
    ) -> str:
        """
        메시지에 대한 응답 생성
        
        Args:
            message: 사용자 메시지
            chat_history: 이전 채팅 기록
            **kwargs: 추가 파라미터
        
        Returns:
            에이전트 응답
        """
        pass
    
    @abstractmethod
    async def stream(
        self, 
        message: str, 
        chat_history: Optional[List[ChatMessage]] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        스트리밍 응답 생성
        
        Args:
            message: 사용자 메시지
            chat_history: 이전 채팅 기록
            **kwargs: 추가 파라미터
        
        Yields:
            응답 청크들
        """
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """
        에이전트 상태 확인
        
        Returns:
            상태 정보
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "status": "healthy",
            "config": self.config.model_dump()
        }
    
    def get_info(self) -> Dict[str, Any]:
        """
        에이전트 정보 반환
        
        Returns:
            에이전트 정보
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "config": self.config.model_dump()
        }
    
    def __str__(self) -> str:
        return f"{self.name} v{self.version}"
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', version='{self.version}')>"


# 기존 채팅 기록 형식을 ChatMessage로 변환하는 유틸리티
def convert_legacy_history(history: List[Dict[str, str]]) -> List[ChatMessage]:
    """
    기존 {"role": "user", "content": "..."} 형식을 ChatMessage로 변환
    
    Args:
        history: 기존 형식의 채팅 기록
    
    Returns:
        ChatMessage 리스트
    """
    return [
        ChatMessage(role=msg["role"], content=msg["content"])
        for msg in history
    ]


def convert_to_legacy_history(messages: List[ChatMessage]) -> List[Dict[str, str]]:
    """
    ChatMessage를 기존 형식으로 변환
    
    Args:
        messages: ChatMessage 리스트
    
    Returns:
        기존 형식의 채팅 기록
    """
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]