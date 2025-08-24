## 핵심 인터페이스

```python
class BaseAgent(ABC):
    @abstractmethod
    async def invoke(self, message: str, chat_history: Optional[List[ChatMessage]] = None, **kwargs) -> str:
        """메시지 응답 생성"""

    @abstractmethod
    async def stream(self, message: str, chat_history: Optional[List[ChatMessage]] = None, **kwargs) -> AsyncGenerator[str, None]:
        """스트리밍 응답 생성"""

    @property
    @abstractmethod
    def name(self) -> str:
        """에이전트 이름"""

    @property
    @abstractmethod
    def description(self) -> str:
        """에이전트 설명"""

```