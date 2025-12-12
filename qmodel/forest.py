"""Forest variant of the Bosatta–Ågren Q-model 

Notes:
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd

from .utils import time_grid

@dataclass(frozen=True)
class ForestParams:
    # Inputs
    l: float          # litter input (t/ha/year)
    q0: float         # initial quality
    r0: float         # initial C/N ratio in litter
    T_C: float        # mean annual temperature (°C)
    fC: float         # microbial C concentration
    fN: float         # microbial N concentration

    # Defaults
    e0: float = 0.25
    h11: float = 0.36
    b: float = 7.0

    # If you want to override u0, set this (otherwise linear T relation is used)
    u0_override: Optional[float] = None

def u0_from_temperature(T_C: float) -> float:
    #Original linear relation
    return 0.075 + 0.014 * float(T_C)

def css_steady_state(p: ForestParams) -> float:
    u0 = p.u0_override if p.u0_override is not None else u0_from_temperature(p.T_C)
    denom = (1.0 - p.e0 - p.e0 * p.h11 * p.b)
    if abs(denom) < 1e-12:
        raise ZeroDivisionError("Denominator (1-e0-e0*h11*b) is ~0; steady state undefined.")
    return p.l / (p.fC * u0 * (p.q0 ** p.b)) * (p.e0 / denom)

def nss_steady_state(p: ForestParams) -> float:
    #steady state
    Css = css_steady_state(p)
    NSS1 = Css * (p.fN / p.fC)
    NSS2 = (p.fN / p.fC - p.r0) * (1.0 - p.e0 - p.e0 * p.h11 * p.b) / (1.0 - p.e0 * p.h11 * p.b) * Css
    return NSS1 - NSS2

def forest_run(
    params: ForestParams,
    n_steps: int = 25,
    dt: float = 1.0,
    t_end: float | None = None,
) -> pd.DataFrame:
    """Run the forest scenario.

    Parameters
    ----------
    params:
        ForestParams
    n_steps:
        Number of discrete steps (intervals). Output length is n_steps+1.
    dt:
        Step length in years (default 1.0).
    t_end:
        If provided, overrides n_steps*dt and spans [0, t_end].

    Returns DataFrame with columns:
        t, q, q_rel, g, h, C, N
    """
    p = params
    u0 = p.u0_override if p.u0_override is not None else u0_from_temperature(p.T_C)

    # Intermediate constants 
    alpha = p.b * p.h11 * p.fC * u0 * (p.q0 ** p.b)
    z = (1.0 - p.e0) / (p.e0 * p.h11)

    t = time_grid(n_steps=n_steps, dt=dt, t_end=t_end)

    # q_rel = q/q0
    q_rel = (1.0 + alpha * t) ** (-1.0 / p.b)
    q = p.q0 * q_rel

    g = q_rel ** z
    h = (p.r0 - p.fN / p.fC) * (q_rel ** (1.0 / (p.e0 * p.h11))) + (p.fN / p.fC) * g

    Css = css_steady_state(p)

    # Soil C and N accumulation towards steady state (as in the script: C = Css*(1-qq**(z-b)))
    C = Css * (1.0 - (q_rel ** (z - p.b)))

    # N formula but sampled on the same time axis.
    denom = (1.0 - p.e0 * p.h11 * p.b)
    if abs(denom) < 1e-12:
        raise ZeroDivisionError("Denominator (1-e0*h11*b) is ~0; N(t) undefined.")
    N = (p.fN / p.fC) * C - (p.fN / p.fC - p.r0) * (p.e0 / denom) * (1.0 - (q_rel ** (1.0 / (p.e0 * p.h11) - p.b))) / (p.fC * u0 * (p.q0 ** p.b))

    return pd.DataFrame({
        "t": t,
        "q": q,
        "q_rel": q_rel,
        "g": g,
        "h": h,
        "C": C,
        "N": N,
    })
