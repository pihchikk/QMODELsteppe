"""Bare-fallow / steppe variant of the Q-model (based on barefallowSTEPPEQ1.py).

Key options:
  - constant Re (analytic q(t) matches the original formula)
  - time-varying Re (iterative update; step ~ year by default)

Outputs:
  - q (absolute), q_rel (=q/q0)
  - Ct (total SOC in bare fallow) and Cpt (plant-derived material pool)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Sequence, Union, Optional
import numpy as np
import pandas as pd

from .utils import time_grid
from .climate import ReLike, constant

@dataclass(frozen=True)
class BareFallowParams:
    l: float = 20.0
    e0: float = 0.303
    q0: float = 0.98
    h11: float = 0.31
    u0: float = 0.49
    Re: float = 1.0  # default constant climate factor
    b0: float = 6.75
    x_silt_pct: float = 27.0
    Css: float = 100.0

def b_from_silt(p: BareFallowParams) -> float:
    return p.b0 + 0.01 * p.x_silt_pct

def qss(p: BareFallowParams) -> float:
    b = b_from_silt(p)
    return p.q0 * (1.0 - p.e0 - p.h11 * p.e0 * b) / (1.0 - p.e0 - p.h11 * p.e0 * (b - 1.0))

def cpss(p: BareFallowParams) -> float:
    b = b_from_silt(p)
    return p.l * (p.e0 / (p.u0 * (p.q0 ** b)))

def _Re_callable(Re: ReLike, seed: Optional[int] = None) -> Callable[[float], float]:
    if callable(Re):
        return Re
    if isinstance(Re, (float, int)):
        return constant(float(Re))
    # sequence
    seq = np.asarray(Re, dtype=float)
    def f(t: float) -> float:
        # assumes t is on the same grid; nearest index
        i = int(round(t))
        i = max(0, min(i, len(seq)-1))
        return float(seq[i])
    return f

def barefallow_run(
    params: BareFallowParams,
    n_steps: int = 200,
    dt: float = 1.0,
    t_end: float | None = None,
    Re: ReLike | None = None,
    *,
    variable_Re_mode: str = "iterative",
) -> pd.DataFrame:
    """Run the bare-fallow scenario.

    Parameters
    ----------
    params:
        BareFallowParams
    n_steps, dt, t_end:
        Time discretization. Default: 200 steps of 1 year.
    Re:
        Climate factor. If None, uses params.Re (constant).
        Can be: float, sequence, or callable Re(t).
    variable_Re_mode:
        - "analytic": always use analytic formula q(t) (best when Re is constant).
        - "iterative": if Re varies with time, update q step-by-step (recommended).

    Returns
    -------
    DataFrame with columns:
        t, Re, q, q_rel, Ct, Cpt
    """
    p = params
    b = b_from_silt(p)

    t = time_grid(n_steps=n_steps, dt=dt, t_end=t_end)

    if Re is None:
        Re = float(p.Re)

    # Prepare Re(t) samples per step (piecewise-constant on [t_i, t_{i+1}))
    if callable(Re):
        Re_vals = np.array([float(Re(float(tt))) for tt in t], dtype=float)
    elif isinstance(Re, (float, int)):
        Re_vals = np.full_like(t, float(Re), dtype=float)
    else:
        Re_arr = np.asarray(Re, dtype=float)
        if len(Re_arr) == len(t):
            Re_vals = Re_arr
        elif len(Re_arr) == n_steps:
            Re_vals = np.concatenate([[Re_arr[0]], Re_arr])
        else:
            raise ValueError("Re sequence length must be n_steps or n_steps+1")

    q = np.empty_like(t, dtype=float)

    if variable_Re_mode == "analytic" or np.allclose(Re_vals, Re_vals[0]):
        # Analytic formula from barefallowSTEPPEQ1.py (exact when Re constant)
        Re0 = float(Re_vals[0])
        q[:] = p.q0 / (1.0 + b * p.h11 * p.u0 * Re0 * t * (p.q0 ** b)) ** (1.0 / b)
    else:
        # Iterative update (recommended for variable Re)
        q[0] = p.q0
        for i in range(1, len(t)):
            Re_i = float(Re_vals[i-1])
            q_prev = float(q[i-1])
            q[i] = q_prev / (1.0 + b * p.h11 * p.u0 * Re_i * dt * (q_prev ** b)) ** (1.0 / b)

    q_rel = q / p.q0

    # Pools (as in the script)
    Cpss = cpss(p)
    Cpt = Cpss * np.exp(-t * (p.e0 / (p.u0 * (p.q0 ** b))))
    exponent = abs((1.0 - p.e0) / (p.h11 * p.e0)) - b
    Ct = p.Css * (q_rel ** exponent)

    return pd.DataFrame({
        "t": t,
        "Re": Re_vals,
        "q": q,
        "q_rel": q_rel,
        "Ct": Ct,
        "Cpt": Cpt,
    })
