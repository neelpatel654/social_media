from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langchain.tools import tool
from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_api_key)


serp_api_key = os.getenv("SERP_API_KEY")


search = GoogleTrendsQueryRun(
    api_wrapper=GoogleTrendsAPIWrapper(serp_api_key=serp_api_key)
)


def get_top_trends_for_query(query: str) -> list[str]:
    system_message = """
    You are a helpful assistant that extracts the main trend title or topic from a user's query to help identify trending or popular subjects.
Given a user's query, return only the one word trend title or topic — concise, specific, and suitable for web search or trend analysis """

    human_message = HumanMessage(
        content=(
            f"user_request: {query} "
        )
    )

    optimized_response = llm.invoke([system_message, human_message])
    optimized_web_request = optimized_response.content
    print("[OPTIMIZE QUERIES] Optimized request:>>>>>>>>>>>>>>>>>>>>",
          optimized_web_request)
    get_google_trends.invoke(optimized_web_request)


@tool(parse_docstring=True)
def get_google_trends(keyword: str) -> dict:
    """
    Fetches Google Trends data for a given keyword.

    Args:
        keyword (str): The keyword or topic to fetch trending search data for.

    Returns:
        Dict: A dictionary containing:
            - 'top_related_queries' (List[str]): Top related search queries
            - 'rising_related_queries' (List[str]): Rising (trending) search queries
            - 'trend_values' (List[int]): List of trend values over time
            - 'date_from' (str): Start date of the trend data
            - 'date_to' (str): End date of the trend data
            - 'min_value' (int): Minimum trend value
            - 'max_value' (int): Maximum trend value
            - 'average_value' (float): Average trend value
            - 'percent_change' (float): Percent change over the period
    """
    print("keyword-------------->>>>>>>>>>", keyword)
    result = search.invoke(keyword)
    print("keyword2-------------->>>>>>>>>>", result)
    rising_queries, top_queries, trend_values = [], [], []
    date_from, date_to = "", ""
    min_value, max_value, avg_value, percent_change = 0, 0, 0.0, 0.0

    for line in result.split('\n'):
        line = line.strip()
        if line.startswith("Date From:"):
            date_from = line.replace("Date From:", "").strip()
        elif line.startswith("Date To:"):
            date_to = line.replace("Date To:", "").strip()
        elif line.startswith("Min Value:"):
            min_value = int(float(line.replace("Min Value:", "").strip()))
        elif line.startswith("Max Value:"):
            max_value = int(float(line.replace("Max Value:", "").strip()))
        elif line.startswith("Average Value:"):
            avg_value = float(line.replace("Average Value:", "").strip())
        elif line.startswith("Percent Change:"):
            percent_change = float(line.replace(
                "Percent Change:", "").replace("%", "").strip())
        elif line.startswith("Trend values:"):
            trend_values = [int(val.strip()) for val in line.replace(
                "Trend values:", "").split(",")]
        elif line.startswith("Rising Related Queries:"):
            rising_queries = [q.strip() for q in line.replace(
                "Rising Related Queries:", "").split(",")]
        elif line.startswith("Top Related Queries:"):
            top_queries = [q.strip() for q in line.replace(
                "Top Related Queries:", "").split(",")]

    print({
        "top_related_queries": top_queries[:5]
    })


result = get_top_trends_for_query("top 5 latest trends on virat kohli")
print(result)
