import os
import sim
import simpy
from functools import partial
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":
    test_params = [(.5, 1.0), (.7, 1.0), (.9, 1.0)]
    pq_2 = [.1, .1815, .2793]
    tq = []
    theoretical_q_len = {}
    agg_resource_df = pd.DataFrame()
    for ns in range(1,3):
        agg_resource_df = pd.DataFrame()
        tq = []

        for (ar, sr), i in zip(test_params, range(0,3)):
            arrival_rate = ar
            service_rate = sr
            num_servers = ns
            rho = arrival_rate / service_rate
            
            print(f"sim variables")
            print(f"arrival_rate: {arrival_rate}")
            print(f"service_rate: {service_rate}")
            print(f"num_servers: {num_servers}\n")

            # theoretical queue_len
            e_queue = (arrival_rate/(num_servers*service_rate))/(1-arrival_rate/(num_servers*service_rate))
            if ns == 2:
                e_queue *= pq_2[i]
            tq.append(e_queue)
            theoretical_q_len[(rho, ns)] = e_queue

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

            resource_df['rho'] = rho
            resource_df['num_servers'] = ns
            agg_resource_df = pd.concat([agg_resource_df, resource_df[['time', 'rho', 'num_servers', 'q_len']]])

            print("results")
            print(f"avg_q_len: {avg_q_len}")
            print(f"avg_resp_time: {avg_resp_time}")
            print(f"server_utilization: {server_utilization}")
            print("\n---------------------\n")

        cwd = os.getcwd()
        g = sns.FacetGrid(agg_resource_df, col="rho")
        g.map(sns.histplot, "q_len", binwidth=1, stat="probability")
        g.figure.subplots_adjust(top=0.8)
        g.figure.suptitle(f"Queue Length with {ns} servers")

        axes = g.axes.flatten()
        for i in range(0,3):
            axes[i].axvline(tq[i], color='r', linestyle='-')

        plt.savefig(f"{cwd}/q_len_hist_{ns}_servers.png")