"""
기본 채팅 에이전트
LangGraph를 사용한 간단한 대화형 에이전트 구현
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from ..settings import get_settings


class AgentState(TypedDict):
    """에이전트 상태 정의"""
    messages: List[BaseMessage]


class DefaultAgent:
    """기본 채팅 에이전트"""
    
    def __init__(self, model_name: str = None):
        """
        Args:
            model_name: 사용할 OpenAI 모델명 (None이면 설정값 사용)
        """
        settings = get_settings()
        self.llm = ChatOpenAI(
            model=model_name or settings.openai_model,
            temperature=settings.openai_temperature,
            api_key=settings.openai_api_key,
            max_tokens=settings.openai_max_tokens
        )
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """LangGraph 워크플로우 구성"""
        workflow = StateGraph(AgentState)
        
        # 노드 추가
        workflow.add_node("chat", self._chat_node)
        
        # 진입점 설정
        workflow.set_entry_point("chat")
        
        # 종료점 설정
        workflow.add_edge("chat", END)
        
        return workflow.compile()
    
    async def _chat_node(self, state: AgentState) -> Dict[str, Any]:
        """채팅 노드 - LLM을 통해 응답 생성"""
        messages = state["messages"]
        
        # OpenAI API 호출
        response = await self.llm.ainvoke(messages)
        
        return {"messages": [response]}
    
    async def invoke(self, message: str, chat_history: List[Dict[str, str]] = None) -> str:
        """
        메시지에 대한 응답 생성
        
        Args:
            message: 사용자 메시지
            chat_history: 이전 채팅 기록 [{"role": "user"|"assistant", "content": "..."}]
        
        Returns:
            에이전트 응답
        """
        # 채팅 기록을 LangChain 메시지 형태로 변환
        messages = []
        
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # 현재 메시지 추가
        messages.append(HumanMessage(content=message))
        
        # 그래프 실행
        result = await self.graph.ainvoke({"messages": messages})
        
        # 마지막 AI 메시지 반환
        return result["messages"][-1].content
    
    async def stream(self, message: str, chat_history: List[Dict[str, str]] = None):
        """
        스트리밍 응답 생성
        
        Args:
            message: 사용자 메시지
            chat_history: 이전 채팅 기록
        
        Yields:
            응답 청크들
        """
        # 채팅 기록을 LangChain 메시지 형태로 변환
        messages = []
        
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        messages.append(HumanMessage(content=message))
        
        # 스트리밍 실행
        async for chunk in self.graph.astream({"messages": messages}):
            if "chat" in chunk and "messages" in chunk["chat"]:
                last_message = chunk["chat"]["messages"][-1]
                if hasattr(last_message, 'content'):
                    yield last_message.content