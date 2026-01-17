# FAST_PATH:
# cheap
# short
# low reasoning
# examples: summaries, definitions, lists
# <---------------------------------------------------->
# DEEP_REASONING:
# complex
# comparative
# analytical
# examples: pros/cons, why, evaluate
# <---------------------------------------------------->
# CLARIFICATION_REQUIRED:
# ambiguous
# underspecified
# vague
# examples: “something general about AI”
# <---------------------------------------------------->
# NOTE FAST_PATH → Groq / small NIM
# NOTE DEEP_REASONING → larger NIM
# NOTE CLARIFICATION → response template
# <---------------------------------------------------->

from enum import Enum
from typing import Dict, Any


class Route(Enum):
    FAST_PATH = "fast_path"
    DEEP_REASONING = "deep_reasoning"
    CLARIFICATION_REQUIRED = "clarification_required"


# <------ Route execution configuration ------>
ROUTE_CONFIG = {
    Route.FAST_PATH: {
        "model_tier": "small",
        "provider": "groq",
        "reasoning": "low",
        "max_tokens": 512,
    },
    Route.DEEP_REASONING: {
        "model_tier": "large",
        "provider": "nim",
        "reasoning": "high",
        "max_tokens": 2048,
    },
    Route.CLARIFICATION_REQUIRED: {
        "model_tier": None,
        "provider": None,
        "reasoning": None,
        "template": "clarification",
    },
}


def route(analysis: dict) -> Route:
    ambiguity = analysis["ambiguity"]
    complexity = analysis["complexity"]
    reasoning = analysis["reasoning"]
    simplicity = analysis["simplicity"]

    # <----- Ambiguity blocks execution ------>
    if ambiguity != "low":
        return Route.CLARIFICATION_REQUIRED

    # <------ Explicit reasoning demand ------>
    if reasoning == "high":
        return Route.DEEP_REASONING

    # <------ Medium complexity without simplification intent ------>
    if complexity == "medium" and simplicity != "high":
        return Route.DEEP_REASONING

    return Route.FAST_PATH




def get_route_payload(route: Route) -> Dict[str, Any]:
    """
    Returns execution metadata for the chosen route.
    """
    return {
        "route": route.value,
        **ROUTE_CONFIG[route],
    }
