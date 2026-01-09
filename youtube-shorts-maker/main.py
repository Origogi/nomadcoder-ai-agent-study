import os
from dotenv import load_dotenv
from youtube_shorts_maker.agent import root_agent

# .env 파일 로드
load_dotenv()

def main():
    print("🚀 YouTube Shorts Maker Agent 실행 중...")
    
    # 간단한 테스트 실행 (필요 시)
    # response = root_agent.run("유튜브 쇼츠 주제로 'AI의 미래'에 대해 기획해줘.")
    # print(response)
    
    print("\n✅ 에이전트가 준비되었습니다.")
    print("웹 인터페이스를 사용하려면 다음 명령어를 실행하세요:")
    print("uv run adk web --reload_agents")

if __name__ == "__main__":
    main()