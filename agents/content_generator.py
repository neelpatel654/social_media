from llm_model.gemini_model import llm


def generate_content(state: dict) -> dict:
    trend = state.get("trend", "")
    prompt = (
        f"Write a short, scroll-stopping social media post description based on the trend: '{trend}'.\n"
        f"The description must:\n"
        f"- Be under 40 words\n"
        f"- Be clear and grammatically correct\n"
        f"- Be highly creative and original (avoid clichés)\n"
        f"- Include a hook or call to action to drive engagement\n"
        f"- Be relevant to the trend and the target audience\n"
        f"- use of emojis and hashtags is encouraged\n"
        f"- Be suitable for Instagram, Twitter, or LinkedIn depending on tone\n"
        f"\nReturn only the description, no explanation or formatting."
    )

    response = llm.invoke(prompt)
    content = response.content.strip()

    return {**state, "content": content}
