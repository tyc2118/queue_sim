# Installation
Create python venv and install required packages with
`pip install -r requirements.txt`

# Usage
Activate and run within venv

## user_sim.py
Single test cases with cmd_line input of arrival rate and service rate. 
Number of servers can be specified as a 3rd parameter if needed, but defaults to 1 if not.

Example usage with arrival rate=0.5, service rate=1.0, num servers=1: `python user_sim.py 0.5 1.0`

## unit_test.py
Sweep rho values: 0.5, 0.7, 0.9 across num servers: 1,2 and plot corresponding histograms with theoretical queue length.
