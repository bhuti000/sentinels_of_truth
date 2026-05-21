from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str) -> str:
    """
    Search the web and return summarized results.
    """
    try:
        response = tavily.search(
            query=query,
            search_depth="basic",
            max_results=3
        )

        results = []

        for item in response["results"]:
            title = item.get("title", "")
            content = item.get("content", "")
            results.append(f"{title}\n{content}")

        return "\n\n".join(results)

    except Exception as e:
        return f"Search failed: {str(e)}"