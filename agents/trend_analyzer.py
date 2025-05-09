from llm_model.gemini_model import llm
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langchain.tools import tool


serper_api_key = os.getenv("SERPER_API_KEY")

search = GoogleSerperAPIWrapper()


def analyze_trend(state: dict) -> dict:

    result = search.run(
        "provide me top 5 latest news or trends on social media of india in 2010")

    prompt = (
        "From the following search result text, extract the single most recent and impactful social media trend "
        "as a short title. Respond with only the trend title, no explanation.\n\n"
        f"{result},e.g., 'Short-Form Video Dominates','Enhanced Content Creation'."
    )

    response = llm.invoke(prompt)
    trend = response.content.strip().strip('"').strip("'")

    return {**state, "trend": trend}

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
