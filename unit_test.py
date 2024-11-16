import sim
import simpy
from functools import partial
import numpy as np
import pandas as pd

if __name__ == "__main__":
    test_params = [(.5, 1.0), (.7, 1.0), (.9, 1.0)]
    agg_resource_data = []
    for ns in range(1,3):
        for ar, sr in test_params:
            arrival_rate = ar
            service_rate = sr
            num_servers = ns
            
            print(f"sim variables")
            print(f"arrival_rate: {arrival_rate}")
            print(f"service_rate: {service_rate}")
            print(f"num_servers: {num_servers}\n")

            resource_data = []
            max_customer_cnt = 10000
            # sim w/o warmup takes roughly 20000
            warmup = 5000
            env = simpy.Environment()

            system = sim.System(env, arrival_rate, service_rate, max_customer_cnt, num_servers, warmup)
            monitor = partial(sim.monitor, resource_data)
            sim.patch_resource(env, system.servers, post=monitor, warmup=warmup)
            env.run()

            cid_df, resource_df = sim.analyze_data(system.cid_data, resource_data)
            avg_resp_time = cid_df.groupby(['cid']).diff().mean()['time']
            server_utilization = resource_df.mean()['util_weight']
            avg_q_len = resource_df.mean()['q_len_weight']

            print("results")
            print(f"avg_q_len: {avg_q_len}")
            print(f"avg_resp_time: {avg_resp_time}")
            print(f"server_utilization: {server_utilization}")
            print("\n---------------------\n")