import sim
import sys
import simpy
from functools import partial

if __name__ == "__main__":
    assert len(sys.argv) == 3 or len(sys.argv) == 4, f"invalid parameter count: {len(sys.argv)}"
    arrival_rate = float(sys.argv[1])
    service_rate = float(sys.argv[2])
    if (len(sys.argv) == 4):
        num_servers = int(sys.argv[3])
    else:
        num_servers = 1

    print("sim variables")
    print(f"arrival_rate: {arrival_rate}")
    print(f"service_rate: {service_rate}")
    print(f"num_servers: {num_servers}")

    resource_data = []
    max_customer_cnt = 10000
    # sim w/o warmup takes roughly 20000
    warmup = 5000
    env = simpy.Environment()

    print("\ninitialize sim")
    system = sim.System(env, arrival_rate, service_rate, max_customer_cnt, num_servers, warmup)
    monitor = partial(sim.monitor, resource_data)
    sim.patch_resource(env, system.servers, post=monitor, warmup=warmup)
    env.run()
    print("sim done.\n")

    cid_df, resource_df = sim.analyze_data(system.cid_data, resource_data)
    avg_resp_time = cid_df.groupby(['cid']).diff().mean()['time']
    server_utilization = resource_df.mean()['util_weight']
    avg_q_len = resource_df.mean()['q_len_weight']

    print("results")
    print(f"avg_q_len: {avg_q_len}")
    print(f"avg_resp_time: {avg_resp_time}")
    print(f"server_utilization: {server_utilization}")