
from groq import Groq


def generate_roadmap(field, level, weeks, hours, api_key):

    client = Groq(api_key=api_key)

    prompt = f"""
    Create a personalized learning roadmap.

    Learning field: {field}
    Skill level: {level}
    Duration: {weeks} weeks
    Available study time: {hours} hours per week

    Write a useful roadmap with these sections:

    1. Learning goals
    2. Week-by-week learning plan
    3. Topics in the correct order
    4. Practical exercises
    5. One final project
    6. Free learning resources
    7. Progress checklist

    Adapt the plan to the user's skill level and time.
    Use simple English, clear headings and bullet points.
    Do not promise mastery if the time is insufficient.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert learning planner. "
                    "Create realistic, structured roadmaps."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=3000
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("The AI returned an empty response.")

    return result
