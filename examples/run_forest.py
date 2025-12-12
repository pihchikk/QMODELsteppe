from qmodel.forest import ForestParams, forest_run
from qmodel.plotting import plot_timeseries

p = ForestParams(
    l=5.0,
    q0=1.0,
    r0=60.0,
    T_C=5.0,
    fC=0.45,
    fN=0.08,
)

df = forest_run(p, n_steps=100, dt=1.0)  # 100 years
print(df.tail())

plot_timeseries(df, x="t", y="C", title="Forest: Soil C accumulation", xlabel="Years", ylabel="C (t/ha)", outfile="forest_C.png")
