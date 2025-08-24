# Agent Lab

ChatGPT와 같은 LLM 기반 채팅 응답 시스템

## 프로젝트 구조

이 프로젝트는 3개의 주요 컴포넌트로 구성됩니다:

### 1. Chat UI (Next.js)
- **위치**: `./chat-ui/src`
- **기술 스택**: Next.js, React, TypeScript, Tailwind CSS
- **역할**: 사용자 인터페이스 제공, 실시간 채팅 UI

### 2. Chat API (Litestar)
- **위치**: `./chat-api/src`
- **기술 스택**: Litestar, Python, FastAPI 호환
- **역할**: API 서버, 비즈니스 로직, 데이터베이스 연동

### 3. Agent Engine (LangGraph)
- **위치**: `./chat-api/src/agents` (초기), 추후 별도 라이브러리화 예정
- **기술 스택**: LangGraph, LangChain, Python
- **역할**: 멀티 에이전트 시스템, LLM 오케스트레이션

## 빠른 시작

```bash
# 저장소 클론
git clone [repository-url]
cd agent-lab

# 백엔드 실행 (자세한 내용은 chat-api/README.md 참조)
cd chat-api && ./setup.sh && pnpm dev

# 프론트엔드 실행 (자세한 내용은 chat-ui/README.md 참조)
cd chat-ui && pnpm install && pnpm dev
```

### 개별 서비스 설정

- **Chat UI**: `chat-ui/README.md` 참조
- **Chat API**: `chat-api/README.md` 참조

## 개발 환경

- **Python**: 3.11+
- **Node.js**: 18+
- **패키지 관리자**: 
  - Python: uv
  - Node.js: pnpm

## 아키텍처

```
agent-lab/
├── chat-ui/           # Next.js 채팅 UI
│   └── src/
├── chat-api/          # Litestar API 서버
│   └── src/
│       └── agents/    # LangGraph 멀티 에이전트 (초기 위치)
├── docs/              # 프로젝트 문서
└── README.md
```

## 기여하기

1. 이슈 생성 또는 기존 이슈 확인
2. 피처 브랜치 생성 (`feature/your-feature-name`)
3. 커밋 (`git commit -m 'Add some feature'`)
4. 푸시 (`git push origin feature/your-feature-name`)
5. Pull Request 생성

## 라이선스

MIT License
