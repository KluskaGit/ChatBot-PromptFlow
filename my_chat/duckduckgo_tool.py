from promptflow.core import tool
from ddgs import DDGS

@tool
def search_worldcup_news(query: str, max_results: int = 5) -> str:
    """
    Wyszukuje informacje o Mistrzostwach Świata 2026 w internecie za pomocą DuckDuckGo.
    """
    try:
        results = []
        worldcup_query = f"Mistrzostwa Świata w piłce nożnej 2026 mundial {query}"
        
        with DDGS() as ddgs:
            for r in ddgs.text(worldcup_query, max_results=max_results):
                title = r.get('title', 'Brak tytułu')
                body = r.get('body', 'Brak treści')
                results.append(f"Tytuł: {title}\nFragment: {body}")
        
        if not results:
            return "Brak wyników wyszukiwania dla tego zapytania."
            
        return "\n\n".join(results)
        
    except Exception as e:
        return f"Wystąpił błąd podczas wyszukiwania w DuckDuckGo: {str(e)}"