from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langchain.tools import tool
from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
from llm_model.gemini_model import llm
from tools.twitter import get_twitter_trends
from langchain_core.messages import HumanMessage
load_dotenv()


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
    return get_google_trends.invoke(optimized_web_request)


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
    print("before result----------->>>>>>>>>>>>", keyword)
    result = search.run(keyword)
    print("after result----------->>>>>>>>>>>>", result)

    top_queries = []

    for line in result.split('\n'):
        line = line.strip()
        if line.startswith("Rising Related Queries:"):
            top_queries = [q.strip() for q in line.replace(
                "Rising Related Queries:", "").split(",")]
    print("trends----------------->>>>>>>>>>>>>>>>>>", top_queries[:5])
    return top_queries[:5]


# def analyze_trend(state: dict) -> dict:
#     result = search.run("India May 2025")
#     prompt = (
#         "From the following Trends search result text, extract the top 5 most recent and rapidly rising social media trends according to . "
#         "Base your selection on a sudden spike in trend values or sharp increases in related query frequency. "
#         "Return only a list of 5 concise trend titles, separated by commas. Do not include any explanation or extra text.\n\n"
#         f"{result}\n\n"
#         "Example output: 'India-Pakistan War, May 2025 Travel Surge, IPL 2025, Election Results 2025, Heatwave Alerts'"
#     )

#     response = llm.invoke(prompt)
#     trends = [t.strip(" \"'") for t in response.content.strip().split(",")][:5]
#     print("trends are: ==========================>", trends)

#     return {**state, "trends": trends}

##################################################################################################################################################

# serper_api_key = os.getenv("SERPER_API_KEY")

# search = GoogleSerperAPIWrapper()


# def analyze_trend(state: dict) -> dict:

#     result = search.run(
#         "provide me top 5 latest news or trends on social media of india in may 2025")

#     prompt = (
#         "From the following search result text, extract the single most recent and impactful social media trend "
#         "as a short title. Respond with only the trend title, no explanation.\n\n"
#         f"{result},e.g., 'Short-Form Video Dominates','Enhanced Content Creation'."
#     )

#     response = llm.invoke(prompt)
#     trend = response.content.strip().strip('"').strip("'")

#     return {**state, "trend": trend}
##################################################################################################################################################
# tools = [search]

# tavily_api_key = os.getenv("TAVILY_API_KEY")

# tavily = TavilySearchResults()
# llm_with_tool = llm.bind_tools(tools=[tavily])

# search = GoogleSerperAPIWrapper()

# @tool
# def get_latest_social_media_trend(query: str) -> str:
#     """Return the most recent high-impact social media trend title."""
#     results = search.run(query)
#     return results[:300]

# tools = [get_latest_social_media_trend]
# llm_with_tool = llm.bind_tools(tools=tools)
# result = llm_with_tool.invoke("latest social media trend")
# print(result)

# def analyze_trend(state: dict) -> dict:
#     query = "Short-form Video Domination:"
#     prompt = (
#         "fetch one of the latest as of current high-impact social media trend "
#         "Respond with only the trend title for {query}, e.g., 'Short-Form Video Dominates','Enhanced Content Creation'."
#     )
#     response = llm_with_tool.invoke(prompt)
#     trend = response.content
#     return {**state, "trend": trend}
