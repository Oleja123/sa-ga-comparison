"""Benchmarking helpers: timing and simple experiment runner"""
import time
from typing import Callable, Any, Dict


def timeit(fn: Callable[..., Any], *args, **kwargs) -> Dict[str, Any]:
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    t1 = time.perf_counter()
    return {"result": out, "time_s": t1 - t0}


def run_experiment(algorithm_fn: Callable[[Any, int], Any], runs: int = 5, **kwargs):
    results = []
    cur_sum : float = 0
    for i in range(runs):
        r = timeit(algorithm_fn, **kwargs)
        results.append(r)
        cur_sum += r["time_s"]
    avg_time = cur_sum / runs if runs > 0 else 0
    return results, avg_time
