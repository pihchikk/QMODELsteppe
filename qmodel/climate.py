"""Climate/forcing helpers.

Here we provide small utilities; you can pass your own callables too.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Sequence, Union, Optional
import numpy as np

ReLike = Union[float, Sequence[float], Callable[[float], float]]

def constant(value: float) -> Callable[[float], float]:
    #Return Re(t)=value."""
    def f(_: float) -> float:
        return float(value)
    return f

def random_uniform(low: float, high: float, seed: Optional[int] = None) -> Callable[[float], float]:
    #Return Re(t) sampled independently from Uniform(low, high) each step (use with iterative update).
    rng = np.random.default_rng(seed)
    def f(_: float) -> float:
        return float(rng.uniform(low, high))
    return f

def arrhenius_multiplier(T_C: float, Ea_kJ_mol: float, Tref_C: float = 10.0, R_kJ_mol_K: float = 0.008314) -> float:
    #Arrhenius temperature multiplier.
    #Returns exp( -Ea/(R*(T+273)) + Ea/(R*(Tref+273)) ).

    T = T_C + 273.0
    Tref = Tref_C + 273.0
    return float(np.exp(-(Ea_kJ_mol/(R_kJ_mol_K*T)) + (Ea_kJ_mol/(R_kJ_mol_K*Tref))))
