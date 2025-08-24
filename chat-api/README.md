# Chat API

Litestar 기반 채팅 API 서버 + LangGraph 멀티 에이전트 시스템

## 기술 스택

- **프레임워크**: Litestar
- **언어**: Python 3.11+
- **패키지 관리**: uv
- **서버**: Uvicorn
- **에이전트**: LangGraph, LangChain
- **CLI**: Typer, Rich

## 설치 및 실행

### 초기 설정

```bash
cd chat-api

# 가상환경 생성 및 의존성 설치
uv sync

# 환경변수 설정
export OPENAI_API_KEY="your-openai-api-key"
```

### API 서버 실행

```bash
# 개발 서버 시작
poe dev

# 또는 직접 실행
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn src.app.main:app --reload --reload-dir src --host 0.0.0.0 --port 8000
```

서버가 시작되면 http://localhost:8000 에서 접근 가능합니다.

### CLI로 에이전트와 대화

```bash
# 기본 에이전트와 대화 시작
poe chat

# 특정 모델 사용
poe chat --model gpt-4

# 시스템 프롬프트 설정
poe chat --system "당신은 도움이 되는 AI 어시스턴트입니다."

# CLI 정보 확인
poe chat-info
```

**CLI 사용법:**
- 일반 메시지 입력 후 Enter
- `/quit`, `/exit` 또는 Ctrl+C로 종료
- 채팅 기록 자동 유지
- 마크다운 형식 응답 렌더링

## 패키지 관리

```bash
# 새 패키지 추가
uv add <package-name>

# 개발 의존성 추가
uv add --dev <package-name>

# 패키지 업데이트
uv sync --upgrade

# 전체 패키지 재설치
rm -rf .venv && uv sync
```

## 개발

### 코드 품질 관리

```bash
# 린트 검사
poe lint

# 코드 포맷팅
poe format

# 테스트 실행
poe test

# 빌드
poe build
```

### 테스트

```bash
# 테스트 실행
pytest

# 커버리지 포함 테스트
pytest --cov=src

# 특정 테스트 실행
pytest tests/test_agents.py -v
```

## API 엔드포인트

### Health Check

- `GET /` - 서비스 상태 확인
- `GET /api/health` - API 헬스 체크

### 채팅 API (예정)

- `POST /api/chat` - 채팅 메시지 전송
- `POST /api/chat/stream` - 스트리밍 채팅

## 프로젝트 구조

```
chat-api/
├── src/
│   ├── app/
│   │   └── main.py           # 애플리케이션 엔트리포인트
│   ├── agents/               # LangGraph 멀티 에이전트
│   │   ├── default/          # 기본 채팅 에이전트
│   │   │   ├── __init__.py
│   │   │   └── agent.py
│   │   ├── cli.py            # CLI 인터페이스
│   │   └── __init__.py
│   ├── api/                  # API 라우터 (예정)
│   ├── core/                 # 핵심 비즈니스 로직 (예정)
│   └── models/               # 데이터 모델 (예정)
├── tests/                    # 테스트 코드
├── pyproject.toml            # 프로젝트 설정
├── uv.lock                   # 패키지 잠금 파일
└── README.md
```

## 환경변수

```bash
# .env 파일 생성
ENVIRONMENT=development
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
OPENAI_API_KEY=your-openai-api-key  # 필수
```

## 사용 가능한 명령어

```bash
# 서버 관련
poe dev              # 개발 서버 시작

# CLI 관련
poe chat             # 기본 에이전트와 대화
poe chat-info        # CLI 정보 확인

# 개발 도구
poe test             # 테스트 실행
poe lint             # 린트 검사
poe format           # 코드 포맷팅
poe build            # 프로젝트 빌드
```

## 에이전트 개발 가이드

### 새로운 에이전트 추가

1. `src/agents/` 하위에 새 디렉토리 생성
2. `agent.py`에 LangGraph 기반 에이전트 구현
3. `__init__.py`에 에이전트 export
4. 필요시 CLI 명령어 추가

### 에이전트 구조 예시

```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: List[BaseMessage]

class MyAgent:
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        # LangGraph 워크플로우 구성
        pass
    
    async def invoke(self, message: str) -> str:
        # 메시지 처리 로직
        pass
```

## 트러블슈팅

### 일반적인 문제

1. **OPENAI_API_KEY 오류**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

2. **패키지 설치 오류**
   ```bash
   rm -rf .venv && uv sync
   ```

3. **포트 충돌**
   ```bash
   poe dev --port 8001  # 다른 포트 사용
   ```

## 기여하기

1. 이슈 생성 또는 기존 이슈 확인
2. 피처 브랜치 생성 (`feature/your-feature-name`)
3. 코드 작성 및 테스트 추가
4. `poe lint && poe format && poe test` 실행
5. 커밋 및 푸시
6. Pull Request 생성