"""
Chat Controller
Litestar Controller를 사용한 채팅 API
"""

import logging
from litestar import Controller, post, get
from litestar.response import Stream
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

from ..models import ChatRequest, ChatResponse, HealthResponse, StreamChunk
from ..services.chat_service import ChatService, ChatRequest as ServiceChatRequest
from ...agents import ChatMessage

logger = logging.getLogger(__name__)


class ChatController(Controller):
    """채팅 컨트롤러"""
    
    path = "/api"
    tags = ["Chat"]
    
    @post("/chat", summary="채팅 메시지 전송")
    async def chat(self, data: ChatRequest, chat_service: ChatService) -> ChatResponse:
        """채팅 메시지 처리"""
        try:
            # API 모델을 서비스 모델로 변환
            chat_history = None
            if data.history:
                chat_history = [
                    ChatMessage(role=msg.role.value, content=msg.content)
                    for msg in data.history
                ]
            
            service_request = ServiceChatRequest(
                message=data.message,
                history=chat_history
            )
            
            # 서비스 호출
            service_response = await chat_service.send_message(service_request)
            
            # 서비스 모델을 API 모델로 변환
            return ChatResponse(
                message=service_response.message,
                model=service_response.model,
                metadata={
                    "agent": service_response.agent_name,
                    "version": service_response.agent_version
                }
            )
            
        except ValueError as e:
            logger.error(f"채팅 요청 처리 실패: {e}")
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="내부 서버 오류가 발생했습니다."
            )
    
    @post("/chat/stream", summary="스트리밍 채팅")
    async def stream_chat(self, data: ChatRequest, chat_service: ChatService) -> Stream:
        """스트리밍 채팅 처리"""
        # API 모델을 서비스 모델로 변환
        chat_history = None
        if data.history:
            chat_history = [
                ChatMessage(role=msg.role.value, content=msg.content)
                for msg in data.history
            ]
        
        service_request = ServiceChatRequest(
            message=data.message,
            history=chat_history
        )
        
        async def generate_stream():
            """스트림 생성기"""
            try:
                async for chunk in chat_service.stream_message(service_request):
                    if chunk:
                        chunk_data = StreamChunk(content=chunk, is_final=False)
                        yield f"data: {chunk_data.model_dump_json()}\n\n"
                
                # 마지막 청크
                final_chunk = StreamChunk(content="", is_final=True)
                yield f"data: {final_chunk.model_dump_json()}\n\n"
                
            except Exception as e:
                logger.error(f"스트림 생성 중 오류: {e}", exc_info=True)
                error_chunk = StreamChunk(content=f"Error: {str(e)}", is_final=True)
                yield f"data: {error_chunk.model_dump_json()}\n\n"
        
        return Stream(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*"
            }
        )
    
    @get("/health", summary="서비스 상태 확인", tags=["Health"])
    async def health_check(self, chat_service: ChatService) -> HealthResponse:
        """헬스 체크"""
        health_info = await chat_service.health_check()
        
        return HealthResponse(
            status=health_info["status"],
            model=health_info["model"],
            agent=health_info["agent"],
            details=health_info.get("details")
        )