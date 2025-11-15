"""Benchmarking helpers: timing and simple experiment runner"""
import time
from typing import Callable, Any, Dict


def timeit(fn: Callable[..., Any], *args, **kwargs) -> Dict[str, Any]:
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    t1 = time.perf_counter()
    return {"result": out, "time_s": t1 - t0}


def run_experiment(algorithm_fn: Callable[..., Dict], runs: int = 5, **kwargs):
    results = []
    for i in range(runs):
        r = timeit(algorithm_fn, **kwargs)
        results.append(r)
    return results
