# opinion_dynamics_BSE

opinion_dynamics_BSE is a Python project built on top of the BSE, [The Bristol
Stock Exchange](https://github.com/davecliff/BristolStockExchange), is a simple minimal simulation of a limit-order-book financial
exchange, developed for teaching.

The aim of this project is to combine two well established fields of research, i.e. opinion dynamics modelling and financial market simulation with automated traders, to create a generator of simulated market data where the automated traders communicate and update their "opinions" according to generally trusted opinion dynamics models.

One motivation is to create a rigorous training dataset for fraud detection on cryptocurrency markets based on previous work at the University of Bristol and another motivation is to provide an agent-based modelling tool for rational and repeatable exploration of issues in "Narrative Economics" as proposed by Nobel Laureate Robert Shiller.

## Usage

```bash
python BSE.py
```

The main program runs in BSE.py, variables are defined at the top for you to change.
By default it uses O-ZIC traders from traders.py.

Originally the BristolStockExchange BSE project was in one file.
I separated the program into 3 files: BSE.py, populate.py, and traders.py.

## License
[MIT](https://choosealicense.com/licenses/mit/)
