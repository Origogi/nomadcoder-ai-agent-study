# YouTube Shorts Maker Agent

Google ADK(Agent Development Kit)를 활용하여 YouTube Shorts 콘텐츠를 기획하고 제작하는 AI 에이전트 프로젝트입니다.

## 🏗️ 아키텍처 다이어그램

```mermaid
graph TD
    %% 노드 스타일 정의
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef agent fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef model fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef storage fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;

    Start[💡 영상 아이디어] --> Planner[✍️ 콘텐츠 기획 에이전트]
    Planner -->|장면 설명| AssetGen{🎨 에셋 생성 에이전트<br/>병렬 에이전트}

    %% 에이전트 클래스 적용
    class Planner,PromptAgent,ImageMaker,VoiceAgent,Editor agent;
    class GPTImage,TTS model;
    class ImageSave,AudioSave,VideoSave storage;
    class FFMPEG process;

    subgraph ImagePipeline [이미지 생성 파이프라인]
        direction TB
        AssetGen -->|이미지 생성 에이전트| PromptAgent[📝 프롬프트 작성 에이전트]
        PromptAgent -->|프롬프트 최적화| ImageMaker[🎨 이미지 제작 에이전트]
        ImageMaker <-->|이미지 프롬프트 / 이미지 파일| GPTImage[🤖 Google GenAI Imagen 3 모델]
        ImageMaker -->|9:16 이미지| ImageSave[🖼️ 이미지 저장]
    end

    subgraph AudioPipeline [음성 생성 파이프라인]
        direction TB
        AssetGen -->|음성 생성 에이전트| VoiceAgent[🎤 음성 생성 에이전트]
        VoiceAgent <-->|텍스트-음성 변환 스크립트 / 오디오 파일| TTS[🗣️ GPT4o Mini TTS]
        VoiceAgent --> AudioSave[🎵 오디오 저장]
    end

    ImageSave -->|수직 이미지| Editor[📦 영상 편집 에이전트]
    AudioSave -->|나레이션 오디오| Editor

    Editor -->|이미지 & 오디오| FFMPEG[🎞️ FFmpeg]
    FFMPEG -->|최종 영상| VideoSave[💾 영상 저장]
    VideoSave --> End[💬 응답]
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
