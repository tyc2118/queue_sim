import time
from numpy import random as rng

class System:
    def __init__(self, arrival_rate, service_rate, max_customer_cnt, num_servers=1):
        self.arrival_time = 1/arrival_rate
        self.num_servers = num_servers
        self.server_list = []

        self.customer_cnt = 0
        self.max_customer_cnt = max_customer_cnt

        for _ in range(self.num_servers):
            self.server_list.append(Server(service_rate))
        
    def start_sim(self):
        for s in self.server_list:
            s.run()

        while (self.customer_cnt < self.max_customer_cnt):
            # find free server else place on random servers queue
            for s in self.server_list:
                if (not s.busy):
                    s.queue_len += 1
                    break
            else:
                self.server_list[rng.randint(self.num_servers)].queue_len += 1
            self.customer_cnt += 1
            time.sleep(rng.exponential(scale=self.arrival_time))

class Server:
    busy = False
    queue_len = 0

    def __init__(self, service_rate):
        self.service_time = 1/service_rate

    def run(self):
        while (self.queue_len > 0):
            self.queue_len -= 1
            self.busy = True
            time.sleep(rng.exponential(scale=self.service_time))
            self.busy = False


if __name__ == "__main__":
    arrival_rate = 1
    service_rate = 1
    max_customer_cnt = 10000
    system = System(arrival_rate, service_rate, max_customer_cnt)

    System.start_sim()