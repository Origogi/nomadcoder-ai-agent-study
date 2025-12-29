# Customer Support AI Agent

## 프로젝트 개요
고객 문의에 따라 목적에 맞는 AI Agent로 연결되는 Customer Support 시스템 실습 프로젝트

## 기술 스택
- Python 3.11+
- uv (패키지 관리)
- OpenAI SDK

## 개발 환경 설정

### 의존성 설치
```bash
uv sync
```

### 환경변수
`.env` 파일에 OpenAI API 키 설정 필요:
```
OPENAI_API_KEY=your-api-key-here
```

### 실행
Streamlit 서버를 백그라운드에서 실행하고 브라우저를 즉시 열려면 다음 명령어를 사용합니다:
```bash
pkill -f "streamlit" || true && nohup uv run streamlit run main.py --server.headless true > streamlit.log 2>&1 & sleep 2 && open http://localhost:8501
```

로그 확인:
```bash
tail -f streamlit.log
```

## 프로젝트 구조
```
customer-support-agent/
├── CLAUDE.md          # 프로젝트 컨텍스트
├── README.md          # 프로젝트 설명
├── pyproject.toml     # Python 프로젝트 설정
├── .env               # 환경변수 (git 제외)
├── .gitignore         # Git 제외 파일
└── main.py            # 메인 진입점
```

## 커밋 컨벤션
- feat: 새로운 기능 추가
- fix: 버그 수정
- docs: 문서 수정
- refactor: 코드 리팩토링
- test: 테스트 추가/수정
