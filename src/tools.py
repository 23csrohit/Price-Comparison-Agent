# Try different import methods based on CrewAI version
try:
    from crewai_tools import ScrapeWebsiteTool, SerperDevTool
    # Initialize tools
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    
except ImportError:
    try:
        from crewai.tools import ScrapeWebsiteTool, SerperDevTool
        # Initialize tools
        search_tool = SerperDevTool()
        scrape_tool = ScrapeWebsiteTool()
        
    except ImportError:
        # Fallback implementation
        import os
        import requests
        from bs4 import BeautifulSoup
        import json
        
        class SerperDevTool:
            def __init__(self):
                self.api_key = os.getenv("SERPER_API_KEY")
                if not self.api_key:
                    raise ValueError("SERPER_API_KEY not found in environment variables")
            
            def run(self, query: str) -> str:
                """Search using Serper API"""
                url = "https://google.serper.dev/search"
                payload = json.dumps({
                    "q": query,
                    "num": 10
                })
                headers = {
                    'X-API-KEY': self.api_key,
                    'Content-Type': 'application/json'
                }
                
                try:
                    response = requests.request("POST", url, headers=headers, data=payload)
                    if response.status_code == 200:
                        return response.text
                    else:
                        return f"Search failed with status code: {response.status_code}"
                except Exception as e:
                    return f"Error during search: {str(e)}"
        
        class ScrapeWebsiteTool:
            def run(self, url: str) -> str:
                """Scrape website content"""
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Get text and clean it
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    return text[:5000]  # Limit to first 5000 characters
                    
                except Exception as e:
                    return f"Error scraping {url}: {str(e)}"
        
        # Initialize fallback tools
        search_tool = SerperDevTool()
        scrape_tool = ScrapeWebsiteTool()

# Make tools available for import
__all__ = ['search_tool', 'scrape_tool']