# YouTube Shorts Maker Agent

Google ADK(Agent Development Kit)를 활용하여 YouTube Shorts 콘텐츠를 기획하고 제작하는 AI 에이전트 프로젝트입니다.

## 🏗️ 아키텍처 다이어그램

```text
💡 영상 아이디어
      │
      ▼
✍️ 콘텐츠 기획 에이전트 (ContentPlannerAgent)
      │
      │ (장면별 스크립트 및 묘사)
      ▼
🎨 에셋 생성 에이전트 (AssetGeneratorAgent - Parallel)
      │
      ├──────────────────────────────────────────┐
      │                                          │
      ▼ (이미지 생성 파이프라인)                   ▼ (음성 생성 파이프라인)
📝 프롬프트 작성 에이전트                     🎤 음성 생성 에이전트
      │                                          │
      ▼                                          ▼
🎨 이미지 제작 에이전트                       🗣️ Gemini 2.5 Flash Native TTS
      │ (Imagen 4.0 모델 연동)                    │
      ▼                                          ▼
🖼️ 이미지 저장 (9:16)                        🎵 오디오 저장 (WAV)
      │                                          │
      └────────────────────┬─────────────────────┘
                           │
                           ▼
                  📦 영상 편집 에이전트 (VideoAssemblerAgent)
                           │
                           ▼
                  🎞️ FFmpeg (이미지+오디오 합성)
                           │
                           ▼
                  💾 최종 영상 저장 (.mp4)
                           │
                           ▼
                         💬 응답
```

## 🚀 주요 기능
- **YouTube Shorts 콘텐츠 기획**: 사용자의 아이디어를 바탕으로 스크립트 및 구성안 생성
- **멀티 에이전트 워크플로우**: 기획, 이미지 생성, 음성 생성, 영상 편집 에이전트가 협업
- **자동화된 영상 제작**: FFmpeg를 활용한 영상 합성 및 렌더링

## 🛠️ 기술 스택
- **Language**: Python 3.13
- **Framework**: google-adk
- **Model**: Gemini 2.0 (google-genai)
- **Tools**: FFmpeg
