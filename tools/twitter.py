from typing import List
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup


@tool(parse_docstring=True)
def get_twitter_trends(location: str = "india") -> List[str]:
    """Fetch top Twitter (X) trending topics for a given location.

    Args:
        location: The location to fetch trends for (e.g., 'india', 'united-states', 'new-york', 'london').

    Returns:
        A list of top 100 trending topics as strings.
    """
    url = f"https://trends24.in/{location}/"
    response = requests.get(url)
    if response.status_code != 200:
        return [f"Error: Failed to fetch trends for {location}. Status code {response.status_code}."]

    soup = BeautifulSoup(response.text, 'html.parser')

    trends = []
    for trend_tag in soup.select('ol.trend-card__list li'):
        trend = trend_tag.get_text(strip=True)
        trends.append(trend)

    if not trends:
        return [f"No trends found for {location}."]

    return trends[:100]
