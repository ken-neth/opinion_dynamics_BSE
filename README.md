# opinion_dynamics_BSE

opinion_dynamics_BSE is a Python project built on top of the BSE, [The Bristol
Stock Exchange](https://github.com/davecliff/BristolStockExchange), is a simple minimal simulation of a limit-order-book financial
exchange, developed for teaching.

The aim of this project is to combine two well established fields of research, i.e. opinion dynamics modelling and financial market simulation with automated traders, to create a generator of simulated market data where the automated traders communicate and update their "opinions" according to generally trusted opinion dynamics models.

One motivation is to create a rigorous training dataset for fraud detection on cryptocurrency markets based on previous work at the University of Bristol and another motivation is to provide an agent-based modelling tool for rational and repeatable exploration of issues in "Narrative Economics" as proposed by Nobel Laureate Robert Shiller.

## Usage

To run the program:
```bash
python BSE.py
```

# Population parameters
```python
N = 20
trader_name = "ZIC"
n_trials = 1
```
# Opinion Dynamics parameters
```python
u_min = 0.2
u_max = 2.0
u_steps = 19

Max_Op = 1
Min_Op = -1

pe_min = 0.025
pe_max = 0.3
pe_steps = 12

model_name = "RA"
```

# Intensity of interactions
```python
mu = 0.2 # used for all models eg. 0.2
delta = 0.25 # used for Bounded Confidence Model eg. 0.1
lmda = 1.0 # used for Relative Disagreement Model eg. 0.1
```

u_e = 0.1 # extremism uncertainty
extreme_distance = 0.2 # how close one has to be to be an "extremist"
Min_mod_op = Min_Op + extreme_distance
Max_mod_op = Max_Op - extreme_distance
plus_neg = [1, 0] # [1, 1] for both pos and neg extremes respectively


#number of iid repetitions of the simulation at each (u,pe) point
sims_per_point = 5
#number of runs to dump as timeseries of opinion for each agent at each (u,pe)
n_dumps = 0

# whether or not to start with extremes
extreme_start = 0

extremes_half = 0 # extremes half way through

# whether or not to calculate y metrics
y_stats = False

# previous average price
prev_avg = 0

D_t = 0



Originally the BristolStockExchange BSE project was in one file.
I separated the program into 3 files: BSE.py, populate.py, and traders.py.

## License
[MIT](https://choosealicense.com/licenses/mit/)
