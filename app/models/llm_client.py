import os
from groq import Groq
from app.routing import Route

# <-------------- Groq client --------------->

def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set")
    return Groq(api_key=api_key)

# <---- Model registry ---------------------->

FAST_MODEL = "llama-3.1-8b-instant"
DEEP_MODEL = "llama-3.3-70b-versatile"

# <-------------- Executor ------------------->

def run(route: Route, query: str) -> tuple[bool, str, str]:
    """
    Executes the query using Groq based on routing decision.

    Returns:
        (success, model_name, response_text)
    """

    # <-------- CLARIFICATION PATH -------->
    if route == Route.CLARIFICATION_REQUIRED:
        return (
            True,
            "none",
            "Your request is unclear. Please clarify what you want:\n"
            "- definition\n"
            "- comparison\n"
            "- step-by-step explanation"
        )

    # <-------- Model selection -------->
    if route == Route.FAST_PATH:
        model = FAST_MODEL
        system_prompt = "Answer briefly and directly."
    else:
        model = DEEP_MODEL
        system_prompt = (
            "You are an expert assistant. "
            "Think carefully, analyze trade-offs, "
            "and give a structured answer."
        )

    # <-------- Execution -------->
    try:
        client = get_client()

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.3,
        )

        response = completion.choices[0].message.content
        response = response.strip() if response else ""

        return True, model, response

    except Exception as e:
        # Log error server-side
        print("GROQ EXECUTION ERROR:", repr(e)) # function to obtain a string e.g.(ValueError('Invalid input))
        return False, model, ""
