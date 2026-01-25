# Travel Advisor Agent Project

이 프로젝트는 사용자의 여행 계획을 돕는 'Travel Advisor Agent'를 개발하는 프로젝트입니다.

## 프로젝트 정보
- **Framework**: [Google ADK](https://github.com/google/adk) (Agent Development Kit)
- **Language**: Python 3.12+
- **Package Manager**: `uv`

## 주요 파일 구조
- `travel_advisor/agent.py`: 에이전트의 메인 로직 및 구성 (Agent, LoopAgent 등)
- `travel_advisor/prompt.py`: 에이전트의 페르소나 및 시스템 프롬프트 정의
- `travel_advisor/tools.py`: 에이전트가 사용할 커스텀 도구 정의
- `main.py`: 에이전트 실행 및 테스트를 위한 엔트리 포인트

## 개발 가이드라인
- **ADK 규칙**: 에이전트 수정 시 `travel_advisor/` 패키지 구조를 유지하며, `__init__.py`를 통해 에이전트 인스턴스를 노출합니다.
- **프롬프트 관리**: 모든 시스템 프롬프트는 `prompt.py`에서 상수로 관리합니다.
- **도구 추가**: 새로운 기능이 필요한 경우 `tools.py`에 함수를 정의하고 에이전트의 `tools` 리스트에 추가합니다.
- **테스트**: `uv run main.py`를 통해 에이전트의 동작을 로컬에서 확인할 수 있습니다.

## 특이사항
- 여행지 추천 시 구체적인 장소명과 특징을 포함하도록 합니다.
- 한국어 답변을 기본으로 합니다.
