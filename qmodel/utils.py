from __future__ import annotations
import numpy as np

def time_grid(n_steps: int, dt: float, t_end: float | None = None) -> np.ndarray:
    """Build a time grid including t=0.

    If t_end is provided, n_steps is the number of intervals and the grid spans [0, t_end].
    Otherwise t_end = n_steps*dt.
    """
    if n_steps <= 0:
        raise ValueError("n_steps must be > 0")
    if dt <= 0:
        raise ValueError("dt must be > 0")
    if t_end is None:
        t_end = n_steps * dt
    if t_end < 0:
        raise ValueError("t_end must be >= 0")
    return np.linspace(0.0, float(t_end), int(n_steps) + 1)
