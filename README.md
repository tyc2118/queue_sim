# queue_sim
M/M/k queue simulator.

## Installation
Create python virtual environment.

```bash
python -m venv {venv_dir}
```

Install required packages.
```
pip install -r requirements.txt
```

## Usage
Activate and run within venv.
```bash
source {venv_dir}/bin/activate
```

### user_sim.py
Single test cases with command line input of arrival rate $\lambda$ and service rate $\mu$. 
Number of servers can be specified as an optional 3rd parameter, but defaults to 1 if unspecified.

```bash
# arrival rate = 0.5
# service rate = 1.0
# num servers = 1
python user_sim.py 0.5 1.0
```

Returns average queue len, average response time, and server utilization

### unit_test.py
Sweep $\rho = \lambda/\mu$ values: 0.5, 0.7, 0.9 across number of servers: 1,2 and plot corresponding histogram distributions with theoretical queue length.
```bash
python unit_test.py
```
