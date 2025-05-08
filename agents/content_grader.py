from llm_model.gemini_model import llm


def grade_content(state: dict) -> dict:
    content = state.get("content", "")

    prompt = (
        f"Evaluate this social media desciption or content for clarity, creativity, and engagement. "
        f"Return a number from 0 to 100 only do not return any floating point number.:\n\n{content}"
    )
    response = llm.invoke(prompt)

    try:
        grade = int("".join([c for c in response.content if c.isdigit()]))
    except ValueError:
        grade = 0

    return {**state, "grade": grade}
