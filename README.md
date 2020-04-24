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

## "BSE.py" parameters

At the top of the file "BSE.py", parameters can be specified for the simulations.

### Population parameters
```python
N = 20 # assumes symmetry, this specifies the number of buyers and sellers respectively
trader_name = "ZIC" # trader names include: "O-ZIC", "ON-ZIC", etcetera (see populate.py)
n_trials = 1  # number of market sessions in simulation (important for ON-ZIC)
```

### Opinion Dynamics parameters
```python
u_min = 0.2 # minimum uncertainty
u_max = 2.0 # maximum uncertainty
u_steps = 19 # number of steps (used for calculating y metrics)

Max_Op = 1 # maximum opinion
Min_Op = -1 # minimum opinion

pe_min = 0.025 # minimum proportion of extremists
pe_max = 0.3  # maximum proportion of extremists
pe_steps = 12 # number of steps (used for calculating y metrics)

model_name = "RA" # Opinion Dynamics model to use

```

### Intensity of interactions
```python
mu = 0.2 # used for all models eg. 0.2
delta = 0.25 # used for Bounded Confidence Model eg. 0.1
lmda = 1.0 # used for Relative Disagreement Model eg. 0.1
```

### Extremist parameters
```python
u_e = 0.1 # extremism uncertainty
extreme_distance = 0.2 # how close one has to be to be an "extremist"
Min_mod_op = Min_Op + extreme_distance
Max_mod_op = Max_Op - extreme_distance
plus_neg = [1, 0] # [1, 1] for both pos and neg extremes respectively

extreme_start = 0 # whether or not to start with extremes
extremes_half = 0 # extremes half way through

```

### Y metric parameters

```python
#number of iid repetitions of the simulation at each (u,pe) point
sims_per_point = 5
#number of runs to dump as timeseries of opinion for each agent at each (u,pe)
n_dumps = 0
# whether or not to calculate y metrics
y_stats = False
```

### Near zero intelligence parameters

```python
prev_avg = 0 # average transaction price from previous trading period

D_t = 0 # Default value of the asset at time t 
```


Originally the BristolStockExchange BSE project was in one file.
I separated the program into 3 files: BSE.py, populate.py, and traders.py.

## License
[MIT](https://choosealicense.com/licenses/mit/)
