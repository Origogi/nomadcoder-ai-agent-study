import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def main():
    # 환경 변수가 잘 로드되었는지 확인 (보안을 위해 일부만 출력)
    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    print("Hello World from Finance Advisor Agent!")
    
    if firecrawl_key:
        print(f"FIRECRAWL_API_KEY loaded: {firecrawl_key[:5]}...")
    if google_key:
        print(f"GOOGLE_API_KEY loaded: {google_key[:5]}...")

if __name__ == "__main__":
    main()