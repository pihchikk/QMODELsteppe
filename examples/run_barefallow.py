from qmodel.barefallow import BareFallowParams, barefallow_run
from qmodel.climate import random_uniform
from qmodel.plotting import plot_timeseries

p = BareFallowParams()

# Constant Re (analytic == iterative here)
df1 = barefallow_run(p, n_steps=200, dt=1.0, Re=0.9, variable_Re_mode="analytic")
plot_timeseries(df1, x="t", y="Ct", title="Bare fallow (constant Re): Ct", xlabel="Years", ylabel="Ct (t/ha)", outfile="bare_Ct_constant.png")

# Variable Re per year (iterative update recommended)
Re_fun = random_uniform(0.7, 0.98, seed=42)
df2 = barefallow_run(p, n_steps=200, dt=1.0, Re=Re_fun, variable_Re_mode="iterative")
plot_timeseries(df2, x="t", y="Ct", title="Bare fallow (variable Re): Ct", xlabel="Years", ylabel="Ct (t/ha)", outfile="bare_Ct_variable.png")

print(df2.head())
