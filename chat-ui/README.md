# Chat UI

Next.js 기반 채팅 사용자 인터페이스

## 기술 스택

- **프레임워크**: Next.js 15 (App Router)
- **언어**: TypeScript
- **스타일링**: Tailwind CSS
- **패키지 관리**: pnpm
- **개발 도구**: ESLint, Turbopack

## 설치 및 실행

### 초기 설정

```bash
cd chat-ui

# 패키지 설치
pnpm install
```

### 개발 서버 실행

```bash
# 개발 서버 시작
pnpm dev

# Turbopack 사용 (더 빠른 개발 서버)
pnpm dev --turbopack

# 특정 포트에서 실행
pnpm dev --port 3001
```

개발 서버가 시작되면 http://localhost:3000 에서 접근 가능합니다.

### 프로덕션 빌드

```bash
# 프로덕션 빌드
pnpm build

# 빌드된 앱 실행
pnpm start

# 빌드 분석
pnpm build --analyze
```

## 패키지 관리

```bash
# 새 패키지 추가
pnpm add <package-name>

# 개발 의존성 추가
pnpm add --dev <package-name>

# 패키지 업데이트
pnpm update

# 패키지 제거
pnpm remove <package-name>

# 의존성 재설치
rm -rf node_modules pnpm-lock.yaml && pnpm install
```

## 개발

### 코드 품질 관리

```bash
# ESLint 검사
pnpm lint

# ESLint 자동 수정
pnpm lint --fix

# 타입 체크
pnpm type-check
```

### 테스트

```bash
# 테스트 실행
pnpm test

# 테스트 감시 모드
pnpm test:watch

# 커버리지 포함 테스트
pnpm test:coverage
```

## 프로젝트 구조

```
chat-ui/
├── src/
│   ├── app/                  # App Router 페이지
│   │   ├── globals.css       # 글로벌 스타일
│   │   ├── layout.tsx        # 루트 레이아웃
│   │   └── page.tsx          # 홈 페이지
│   ├── components/           # 재사용 가능한 컴포넌트
│   │   ├── ui/               # 기본 UI 컴포넌트
│   │   ├── chat/             # 채팅 관련 컴포넌트
│   │   └── layout/           # 레이아웃 컴포넌트
│   ├── hooks/                # 커스텀 훅
│   ├── lib/                  # 유틸리티 함수
│   ├── store/                # 상태 관리
│   └── types/                # TypeScript 타입 정의
├── public/                   # 정적 파일
├── tailwind.config.ts        # Tailwind 설정
├── next.config.js            # Next.js 설정
├── package.json              # 패키지 정보
└── README.md
```

## 환경변수

```bash
# .env.local 파일 생성
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NODE_ENV=development
```

## 사용 가능한 스크립트

```bash
pnpm dev          # 개발 서버 시작
pnpm build        # 프로덕션 빌드
pnpm start        # 프로덕션 서버 시작
pnpm lint         # ESLint 검사
pnpm test         # 테스트 실행
pnpm type-check   # TypeScript 타입 체크
```

## 트러블슈팅

### 일반적인 문제

1. **패키지 설치 오류**
   ```bash
   rm -rf node_modules pnpm-lock.yaml
   pnpm install
   ```

2. **타입 오류**
   ```bash
   pnpm type-check
   # TypeScript 설정 확인
   ```

3. **빌드 오류**
   ```bash
   rm -rf .next
   pnpm build
   ```

4. **포트 충돌**
   ```bash
   pnpm dev --port 3001
   ```

## 기여하기

1. 이슈 생성 또는 기존 이슈 확인
2. 피처 브랜치 생성 (`feature/your-feature-name`)
3. 컴포넌트 작성 및 테스트 추가
4. `pnpm lint && pnpm type-check && pnpm test` 실행
5. 커밋 및 푸시
6. Pull Request 생성

## 배포

### Vercel 배포

```bash
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

### 환경변수 설정

Vercel 대시보드에서 다음 환경변수를 설정:
- `NEXT_PUBLIC_API_URL`: Chat API 서버 URL
- `NEXT_PUBLIC_WS_URL`: WebSocket URL