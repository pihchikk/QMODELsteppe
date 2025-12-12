"""CLI to run the models and save outputs.

Examples:
  python -m qmodel.cli forest --l 5 --q0 1 --r0 60 --T 5 --fC 0.5 --fN 0.08 --n_steps 100 --dt 1 --out out_forest.csv
  python -m qmodel.cli barefallow --n_steps 200 --dt 1 --Re 0.9 --out out_bare.csv
"""

from __future__ import annotations
import argparse
import pandas as pd

from .forest import ForestParams, forest_run
from .barefallow import BareFallowParams, barefallow_run

def _add_common_time_args(p: argparse.ArgumentParser):
    p.add_argument("--n_steps", type=int, default=25)
    p.add_argument("--dt", type=float, default=1.0)
    p.add_argument("--t_end", type=float, default=None)
    p.add_argument("--out", type=str, default=None)

def main(argv=None):
    ap = argparse.ArgumentParser(prog="qmodel")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_f = sub.add_parser("forest")
    ap_f.add_argument("--l", type=float, required=True)
    ap_f.add_argument("--q0", type=float, required=True)
    ap_f.add_argument("--r0", type=float, required=True)
    ap_f.add_argument("--T", type=float, required=True)
    ap_f.add_argument("--fC", type=float, required=True)
    ap_f.add_argument("--fN", type=float, required=True)
    ap_f.add_argument("--b", type=float, default=7.0)
    ap_f.add_argument("--e0", type=float, default=0.25)
    ap_f.add_argument("--h11", type=float, default=0.36)
    ap_f.add_argument("--u0", type=float, default=None)
    _add_common_time_args(ap_f)

    ap_b = sub.add_parser("barefallow")
    ap_b.add_argument("--n_steps", type=int, default=200)
    ap_b.add_argument("--dt", type=float, default=1.0)
    ap_b.add_argument("--t_end", type=float, default=None)
    ap_b.add_argument("--Re", type=float, default=None)
    ap_b.add_argument("--variable_Re_mode", type=str, default="iterative", choices=["iterative", "analytic"])
    ap_b.add_argument("--out", type=str, default=None)

    args = ap.parse_args(argv)

    if args.cmd == "forest":
        fp = ForestParams(
            l=args.l, q0=args.q0, r0=args.r0, T_C=args.T, fC=args.fC, fN=args.fN,
            b=args.b, e0=args.e0, h11=args.h11, u0_override=args.u0
        )
        df = forest_run(fp, n_steps=args.n_steps, dt=args.dt, t_end=args.t_end)
    else:
        bp = BareFallowParams()
        df = barefallow_run(bp, n_steps=args.n_steps, dt=args.dt, t_end=args.t_end, Re=args.Re, variable_Re_mode=args.variable_Re_mode)

    if args.out:
        df.to_csv(args.out, index=False)
    else:
        print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
