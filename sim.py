from numpy import random as rng
import simpy
from functools import wraps
import pandas as pd

class System:
    def __init__(self, env, arrival_rate, service_rate, max_customer_cnt, num_servers, warmup):
        self.warmup = warmup
        self.env = env
        self.arrival_time = 1/arrival_rate
        self.service_time = 1/service_rate
        self.max_customer_cnt = max_customer_cnt
        self.num_servers = num_servers

        self.cid_data = []

        self.servers = simpy.Resource(env, capacity=self.num_servers)

        env.process(self.customers(env))

    def customers(self, env):
        while (env.now < self.warmup):
            env.process(self.request(env, cid=-1))
            yield self.env.timeout(rng.exponential(scale=self.arrival_time))

        cid = 0
        for _ in range(self.max_customer_cnt):
            env.process(self.request(env, cid))
            yield self.env.timeout(rng.exponential(scale=self.arrival_time))
            cid += 1

    def request(self, env, cid):
        if (env.now > self.warmup):
            self.cid_data.append((env.now, cid))
        with self.servers.request() as req:
            yield req
            yield env.timeout(rng.exponential(scale=self.service_time))
            if (env.now > self.warmup):
                self.cid_data.append((env.now, cid))

def patch_resource(env, resource, pre=None, post=None, warmup=0):
    """Patch *resource* so that it calls the callable *pre* before each
    put/get/request/release operation and the callable *post* after each
    operation.  The only argument to these functions is the resource
    instance.
    code from simpy documentation.
    """

    def get_wrapper(func):
        # Generate a wrapper for put/get/request/release
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This is the actual wrapper
            # Call "pre" callback
            if pre and env.now > warmup:
                pre(resource)

            # Perform actual operation
            ret = func(*args, **kwargs)

            # Call "post" callback
            if post and env.now > warmup:
                post(resource)

            return ret
        return wrapper


    # Replace the original operations with our wrapper
    for name in ['request', 'release']:
        if hasattr(resource, name):
            setattr(resource, name, get_wrapper(getattr(resource, name)))

def monitor(data, resource):
    """This is our monitoring callback.
    code from simpy documentation.
    """
    item = (
        resource._env.now,  # The current simulation time
        resource.count,  # The number of users
        len(resource.queue),  # The number of queued processes
    )
    data.append(item)

def analyze_data(cid_data, resource_data):
    cid_df = pd.DataFrame(cid_data, columns = ['time', 'cid'])

    resource_df = pd.DataFrame(resource_data, columns = ['time', 'users', 'q_len'])
    resource_df['time_diff'] = resource_df['time'].shift(-1) - resource_df['time']
    resource_df.dropna(inplace=True)
    resource_df['q_len_weight'] = resource_df['q_len'] * resource_df['time_diff']
    resource_df['util_weight'] = resource_df['users'] * resource_df['time_diff']

    return (cid_df, resource_df)
