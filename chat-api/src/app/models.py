"""
API 모델 정의
Pydantic 모델을 사용한 요청/응답 스키마
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """메시지 역할"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessageRequest(BaseModel):
    """채팅 메시지 요청"""
    role: MessageRole = Field(..., description="메시지 역할")
    content: str = Field(..., description="메시지 내용")


class ChatRequest(BaseModel):
    """채팅 요청"""
    message: str = Field(..., description="사용자 메시지", min_length=1)
    history: Optional[List[ChatMessageRequest]] = Field(
        default=None, 
        description="이전 대화 기록"
    )


class ChatResponse(BaseModel):
    """채팅 응답"""
    message: str = Field(..., description="에이전트 응답")
    model: str = Field(..., description="사용된 모델명")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="추가 메타데이터"
    )


class StreamChunk(BaseModel):
    """스트림 청크"""
    content: str = Field(..., description="응답 내용 조각")
    is_final: bool = Field(default=False, description="마지막 청크 여부")


class HealthResponse(BaseModel):
    """상태 확인 응답"""
    status: str = Field(..., description="서비스 상태")
    model: str = Field(..., description="사용 중인 모델")
    agent: str = Field(..., description="사용 중인 에이전트")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="상세 정보"
    )


class ErrorResponse(BaseModel):
    """에러 응답"""
    error: str = Field(..., description="에러 타입")
    message: str = Field(..., description="에러 메시지")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="에러 상세 정보"
    )