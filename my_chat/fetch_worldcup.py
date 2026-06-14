from promptflow.core import tool
from ddgs import DDGS

@tool
def fetch_worldcup_news(query: str = "") -> str:
    """
    Pobiera informacje z wyszukiwarki DuckDuckGo,
    koncentrując się na Mundialu 2026.
    """
    # Nie musimy już tak agresywnie wycinać słów kluczowych, 
    # ponieważ silnik wyszukiwarki dobrze radzi sobie z naturalnym językiem.
    search_query = f"Mistrzostwa Świata w Piłce Nożnej 2026 {query}".strip()
    
    try:
        # Inicjalizacja klienta DuckDuckGo i pobranie 5 pierwszych wyników (tekstowych)
        results = DDGS().text(search_query, region='pl-pl', safesearch='off', max_results=5)
        
        if not results:
            return "Brak nowych informacji w wyszukiwarce DuckDuckGo na ten temat."
            
        # Wyciągamy zawartość 'body' (snippet/opis) z każdego wyniku
        snippets = [result.get('body', '') for result in results if 'body' in result]
        
        return "Znalezione informacje (jako kontekst):\n- " + "\n- ".join(snippets)
    except Exception as e:
        return f"Wystąpił błąd podczas wyszukiwania w DuckDuckGo: {e}"