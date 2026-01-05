import dotenv

dotenv.load_dotenv()
import re
import os
from firecrawl import FirecrawlApp


def web_search_tool(query: str):
    """
    Web Search Tool.
    Args:
        query: str
            The query to search the web for.
    Returns
        A list of search results with the website content in Markdown format.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        return "Error: FIRECRAWL_API_KEY is not set in environment variables."
        
    app = Firecrawl(api_key=api_key)

    try:
        # v2 search에서는 scrape_options를 통해 마크다운 포맷을 지정합니다.
        # 일부 버전에서는 scrape=True 파라미터가 필요할 수 있습니다.
        response = app.search(
            query=query,
            limit=5,
            scrape_options={"formats": ["markdown"]},
        )
    except Exception as e:
        return f"Error using tool: {e}"

    cleaned_chunks = []
    
    # response가 SearchData 객체일 경우 web 속성에 접근, 아닐 경우 빈 리스트
    search_results = getattr(response, "web", []) or []

    for result in search_results:
        # 결과가 객체인 경우와 딕셔너리인 경우 모두 대응
        if isinstance(result, dict):
            title = result.get("title", "")
            url = result.get("url", "")
            markdown = result.get("markdown", "")
        else:
            title = getattr(result, "title", "")
            url = getattr(result, "url", "")
            markdown = getattr(result, "markdown", "") or getattr(result, "description", "")

        if not markdown:
            continue

        # 마크다운 텍스트 정제
        cleaned = re.sub(r"\\+|\n+", " ", markdown).strip()
        cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned) # 중복 공백 제거

        cleaned_result = {
            "title": title,
            "url": url,
            "markdown": cleaned[:1000],
        }

        cleaned_chunks.append(cleaned_result)

    return cleaned_chunks[:5]