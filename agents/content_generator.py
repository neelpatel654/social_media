from llm_model.gemini_model import llm


def generate_content(state: dict) -> dict:
    trend = state.get("trend", "")
    prompt = (
        f"Write a short, catchy, and creative description for a social media post about the trend: '{trend}'. "
        "The description should be no more than 40 words, clear, engaging, and suitable for grading on a scale of 0 to 100 for quality."
    )
    response = llm.invoke(prompt)
    content = response.content.strip()
    return {**state, "content": content}
