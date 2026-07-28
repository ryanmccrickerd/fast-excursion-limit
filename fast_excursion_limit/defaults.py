MATURITY_PATHWISE = 0.25
MATURITY_TOUCHES = 0.08

# step_size = delta_scale * maturity
DELTA_SCALE_PATHWISE = 1e-6
DELTA_SCALE_TOUCHES = 1e-5

# Essentially selected so that figure 4 looks reasonable
SEED = 20

# HestonRandomODE._simulate_next's gradient floor. Too high and the simulation is not
# faithful to the model, too low and we must take the step size delta down too. It's not
# a big deal for our purposes; both 1e-2 and 1e-4 look fine too.
EPSILON = 1e-3

# Loosely aligned with one month EURUSD vanilla options at the time of writing.
EXAMPLE_PARAMS_FEH = {
    "spot_price": 1.16,
    "domestic_rate": 0.05,
    "foreign_rate": 0.02,
    "sigma": 0.07,
    "rho": 0.05,
    "gamma": 0.20,
}
EXAMPLE_PARAMS_ODE = {**EXAMPLE_PARAMS_FEH, "reversion": 1.0}

# figures.yml workflow overrides number of paths via papermill
NUM_PATHS_TOUCHES = 100
