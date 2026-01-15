import time
from collections import defaultdict

_metrics = {
    "total_requests": 0,
    "routes": defaultdict(int),
    "models": defaultdict(int),
    "latencies": defaultdict(list),
}


def record_request(route: str, model: str):
    _metrics["total_requests"] += 1
    _metrics["routes"][route] += 1
    _metrics["models"][model] += 1
    
    
def record_latency(route: str, latency_ms: float):
    _metrics["latencies"][route].append(latency_ms)
    

def get_metrics() -> dict:
    avg_latency = {
        route: round(sum(times) / len(times), 2)
        for route, times in _metrics["latencies"].items()
        if times
    }
    
    return {
        "total_requests": _metrics["total_requests"],
        "route": dict(_metrics["routes"]),
        "models": dict(_metrics["models"]),
        "avg_latency_ms": avg_latency,
    }
    
# <--------------------- timing helper ---------------------->

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        self.end = time.perf_counter()
        self.elapsed_ms = (self.end - self.start) * 1000