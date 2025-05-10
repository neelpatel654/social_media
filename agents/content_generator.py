from llm_model.gemini_model import llm
import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
load_dotenv()

serper_api_key = os.getenv("SERPER_API_KEY")

tools = [{"tool": GoogleSerperAPIWrapper(
), "description": "Google Serper API for trending information"}]

llm_with_tool = llm.bind_tools(tools=tools)


def generate_content(state: dict) -> dict:
    trend = state.get("trend", "")
    prompt = (
        f"Write a short, scroll-stopping social media post description based on the trend: '{trend}'.\n"
        f"The description must:\n"
        f"Use only Google serper tool for latest trending information for web serach."
        f"- Be under 40 words\n"
        f"- Be clear and grammatically correct\n"
        f"- Be highly creative and original (avoid clichés)\n"
        f"- Include a hook or call to action to drive engagement\n"
        f"- Be relevant to the trend and the target audience\n"
        f"- use of emojis and hashtags is encouraged\n"
        f"- Be suitable for Instagram, Twitter, or LinkedIn depending on tone\n"
        f"- e.g.,'👀 Blink and it's viral! 📱 Short-form video is rewriting the rules of engagement. Are you creating scroll-stopping content or just watching it fly by? ⚡👇 #ShortFormTakeover #VideoMarketing #ContentGame #SocialMediaTrends' "
        f"\nReturn only the description, no explanation or formatting."

    )

    response = llm.invoke(prompt)

    content = response.content.strip()

    return {**state, "content": content}
