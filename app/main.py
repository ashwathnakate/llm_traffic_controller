from fastapi import FastAPI
from pydantic import BaseModel
import os

# <-------------- internal imports --------------->
from app.analyzer import analyze
from app.routing import route, Route
from app.models.llm_client import run
from app.metrics import (
    record_request,
    record_latency,
    get_metrics,
    Timer
)

app = FastAPI(title="LLM Traffic COntroller")


class QueryRequest(BaseModel):
    query: str
    
@app.post("/query")
@app.post("/query")
def handle_query(payload: QueryRequest):
    analysis = analyze(payload.query)
    route_decision = route(analysis)

    with Timer() as timer:
        success, model_used, answer = run(route_decision, payload.query)

    # ---- HARD GUARD: never return empty or failed responses ----
    if not success:
        answer = (
            "I couldn't generate a reliable response. "
            "Please rephrase or be more specific."
        )

    record_request(route_decision.value, model_used)
    record_latency(route_decision.value, timer.elapsed_ms)

    return {
        "route": route_decision.value,
        "model": model_used,
        "latency_ms": round(timer.elapsed_ms, 2),
        "analysis": analysis,
        "answer": answer
    }


@app.get("/metrics")
def metrics():
    return get_metrics()