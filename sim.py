from numpy import random as rng
import simpy

class System:
    def __init__(self, env, arrival_rate, service_rate, max_customer_cnt, num_servers=1):
        self.env = env
        self.arrival_time = 1/arrival_rate
        self.service_time = 1/service_rate
        self.num_servers = num_servers

        self.server_list = []
        self.servers = simpy.Resource(env, capacity=self.num_servers)

        self.max_customer_cnt = max_customer_cnt
        env.process(self.customers(env))

    def customers(self, env):
        for _ in range(self.max_customer_cnt):
            env.process(self.request(env))
            yield self.env.timeout(rng.exponential(scale=self.arrival_time))

    def request(self, env):
        with self.servers.request() as req:
            yield req
            yield env.timeout(rng.exponential(scale=self.service_time))

if __name__ == "__main__":
    print("setup variables.")
    arrival_rate = 1
    service_rate = 1
    max_customer_cnt = 10000
    env = simpy.Environment()

    print("initialize sim")
    system = System(env, arrival_rate, service_rate, max_customer_cnt)
    env.run()
    print("done.")