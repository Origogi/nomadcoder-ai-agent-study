from crewai.tools import tool
from crewai_tools import SerperDevTool
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

search_tool = SerperDevTool()


@tool
def scrape_tool(url: str):
    """
    Use this when you need to read content from a web page.
    Returns the content of a website, in case the website is not accessible, returns "No Content".
    Input should be a `url` string. for example: ("https://www.apecceosummitkorea2025.com/)
    """

    print(f"Scraping content from: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        html = ""
        try:
            page.goto(url, timeout=15000)  # 15 seconds timeout
            time.sleep(2)  # Wait for 2 seconds to ensure the page loads completely
            html = page.content()
        except Exception as e:
            print(f"Error accessing {url}: {e}")
            html = "No Content"
        finally:
            browser.close()

        soup = BeautifulSoup(html, 'html.parser')

        unwanted_tags = [
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
            "iframe",
            "form",
            "button",
            "input",
            "select",
            "textarea",
            "img",
            "svg",
            "canvas",
            "audio",
            "video",
            "embed",
            "object",
        ]
        
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
    
        content = soup.get_text(separator=' ', strip=True)

        return content if content else "No Content"
