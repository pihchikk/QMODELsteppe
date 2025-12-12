# Q-model (Bosatta–Ågren) — refactored v2

This folder contains a small Python package `qmodel/` with two scenarios:

- `qmodel.forest.forest_run` — based on `forestQ1.py`
- `qmodel.barefallow.barefallow_run` — based on `barefallowSTEPPEQ1.py`

## Install (editable, local)
From the folder root:
```bash
python -m pip install -e .
```

## Quick run
```bash
python -m qmodel.cli forest --l 5 --q0 1 --r0 60 --T 5 --fC 0.45 --fN 0.08 --n_steps 100 --dt 1
python -m qmodel.cli barefallow --n_steps 200 --dt 1 --Re 0.9 --variable_Re_mode analytic
```

The discretization is controlled by `n_steps` and `dt`. By default, `dt=1` year so each step is one year.
