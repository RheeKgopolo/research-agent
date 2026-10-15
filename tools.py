"""Plain Python functions exposed to the LLM as tools.

aisuite turns each function's signature + docstring into a tool schema,
so keep type hints and docstrings accurate.
"""
import os


def wikipedia_search(query: str, sentences: int = 5) -> str:
    """Search Wikipedia and return a short summary of the best-matching article.

    Args:
        query: What to look up.
        sentences: How many summary sentences to return.
    """
    import wikipedia

    wikipedia.set_user_agent("AgenticLabs/1.0 (learning project)")
    try:
        title = wikipedia.search(query, results=1)
        if not title:
            return f"No Wikipedia results for '{query}'."
        page = wikipedia.page(title[0], auto_suggest=False)
        summary = wikipedia.summary(title[0], sentences=sentences, auto_suggest=False)
        return f"{page.title} ({page.url})\n{summary}"
    except Exception as e:  # disambiguation, network, etc.
        return f"Wikipedia error for '{query}': {e}"


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web with Tavily and return titles, URLs and snippets.

    Args:
        query: The search query.
        max_results: Number of results to return.
    """
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return "web_search unavailable: TAVILY_API_KEY not set. Use wikipedia_search instead."
    from tavily import TavilyClient

    res = TavilyClient(api_key=key).search(query, max_results=max_results)
    lines = [f"- {r['title']} ({r['url']}): {r['content'][:300]}" for r in res.get("results", [])]
    return "\n".join(lines) or "No results."


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression, e.g. '(12.5 * 4) / 3'.

    Args:
        expression: Arithmetic using numbers and + - * / ( ) . only.
    """
    if not set(expression) <= set("0123456789+-*/(). "):
        return "Only numbers and + - * / ( ) are allowed."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


TOOLS = [wikipedia_search, web_search, calculator]
