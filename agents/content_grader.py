from llm_model.gemini_model import llm


def grade_content(state: dict) -> dict:
    content = state.get("content", "")

    prompt = (
        f"Evaluate the following social media description or content. Grade it from 0 to 100 (integer only, no decimals) based on the following criteria:\n"
        f"1. Clarity: Is the message easy to read and free of grammar or spelling errors?\n"
        f"2. Creativity: Is the content original, catchy, or emotionally appealing?\n"
        f"3. Engagement: Does it include a call to action, question, or hook that encourages interaction?\n\n"
        f"4. Also consider used Hashtags and emojis to enhance the content.\n\n"
        f"Content:\n{content}\n\n"
        f"Only return the final score as a whole number from 0 to 100."
    )
    response = llm.invoke(prompt)

    try:
        grade = int("".join([c for c in response.content if c.isdigit()]))
    except ValueError:
        grade = 0

    return {**state, "grade": grade}
