import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    print("Hello from hello-langgraph!")
    
    # Check if OPENAI_API_KEY is loaded
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("OPENAI_API_KEY is loaded.")
    else:
        print("Please set OPENAI_API_KEY in your .env file.")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
