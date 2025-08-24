# CLAUDE.md — Agent Lab 프로젝트 개요

## 1. 프로젝트 개요

- **프로젝트 이름(가칭)**: Agent Lab
- **목표**:  
  - 내부적으로 사용할 수 있는 **Multi Agent Platform** 구축  
  - 이를 기반으로 한 **AI Chat Service (ChatGPT 유사 서비스)** 구현  
  - 작은 MVP → 점진적 확장 → 사내 공식 프로젝트로 발전  

---

## 2. 만들려는 것

### 2.1 Multi Agent Platform
- **기능**
  - Agent 생성, 공유, 협업, 평가, 실행, 배포, 모니터링
  - 외부 프레임워크(LangGraph, Google ADK, CrewAI, Autogen 등)로 만든 Agent도 등록 가능
  - Agent 간 통신은 **A2A 프로토콜(Agent-to-Agent)** 기반
  - MCP(Model Context Protocol) 기반 Tool, Context Provider도 공유 가능
- **가치**
  - 다른 부서에서 Multi Agent 서비스를 쉽고 빠르게 만들 수 있도록 지원
  - 사내 AI 자산을 모아두는 “Agent Pool” 역할 수행

### 2.2 Multi Agent Framework
- **기능**
  - 여러 Agent를 조합해 협업/오케스트레이션 할 수 있는 프레임워크
  - 다른 사람이 만든 Agent/Tool을 import하여 활용 가능
- **가치**
  - Multi Agent System(MAS) 구현의 진입장벽을 낮춤
  - 팀/개인별 다양한 실험 가능

### 2.3 AI Chat Service (MVP)
- **기능**
  - 일반 대화
  - 웹 검색, 딥리서치
  - 코드 실행/Artifact 생성
  - 이미지 생성
- **가치**
  - 사내에서 가장 먼저 쓸 수 있는 “눈에 보이는 서비스”
  - 플랫폼 성능과 안정성을 증명하는 테스트베드

---

## 3. 진행 계획 (점진적 접근)

### 단계별 로드맵
1. **MVP (AI Chat Service)**
   - 백엔드: Litestar + SQLAlchemy (async, UoW/Repo)
   - 프론트엔드: Next.js(App Router) + React + Tailwind
   - 기본 기능: 채팅, 파일 첨부, 웹 검색, 코드 실행
   - 최소한의 Agent 실행 기능 포함 (LangGraph 기반)

2. **Platform 기본 골격**
   - Agent Registry (등록/조회/버전관리)
   - Agent 실행 환경 (Sandbox, A2A 통신)
   - MCP Tool/Context Provider 등록/공유 기능

3. **Multi Agent Framework**
   - Agent 조합 및 오케스트레이션 엔진
   - 평가 시스템 (테스트셋, 성능 리더보드)
   - Agent-to-Agent 통신 최적화 (로드밸런싱, 큐/브로커)

4. **사내 확장**
   - 다양한 팀에서 Agent 제작/등록
   - 사내 공식 플랫폼으로 제안 및 확산

---

## 4. 개발 방식

- **작게 만들고 빠르게 개선**
  - 완벽한 플랫폼이 아니라, **돌아가는 최소 시스템**부터
- **점진적 확장**
  - Chat Service → Platform 골격 → Framework → 공식화
- **배우면서 성장**
  - 단순히 결과물이 아니라, 아키텍처/운영/UX까지 학습 및 기록
- **협업/리뷰 친화적 구조**
  - ADR(Architecture Decision Record) 기록
  - 문서화/README를 통해 누가 와도 이해할 수 있게 유지

---

## 5. 내가 기대하는 효과

- **단기**
  - 직접 만든 ChatGPT 유사 서비스 운영 가능
  - Multi Agent 기반의 내부 PoC 서비스 실험
- **중기**
  - 사내에서 Agent/Tool/Context 공유·재사용 생태계 조성
  - Multi Agent 프로젝트 개발 속도/성능 향상
- **장기**
  - 회사의 공식 **AI Agent Platform**으로 자리잡기
  - 커리어적으로 “사내 AI Agent 플랫폼 창시자” 포지션 확보

---
_최초 정리: 2025-08-24_

- 30줄 이상의 코드를 구현하기 전에는, 먼저 어떤식으로 구현할지 계획을 나한저 먼저 이야기하고 허락받아.