import math
from typing import *
import numpy as np
import collections


class Distributor:

    def custom_distribution(self, min_num: int, max_num: int, traces_num: int, probabilities: [float]):
        if probabilities is None:
            raise ValueError("custom probabilities must be provided")
        s = sum(probabilities)
        if s != 1:
            raise ValueError("sum of provided list must be 1")
        prob_len = len(probabilities)
        prefixes = (max_num + 1) - min_num
        if prob_len != prefixes:
            raise ValueError(
                f"Number of probabilities provided are {prob_len} but min and max difference is {prefixes}")
        return self.__distribute_random_choices(min_num, max_num, traces_num, probabilities)

    def uniform_distribution(self, min_num, max_num, traces_num: int):
        probabilities = self.__get_uniform_probabilities((max_num + 1) - min_num)
        return self.custom_distribution(min_num, max_num, traces_num, probabilities)

    def normal_distribution(self, mu, sigma, num_traces: int):
        trace_lens = np.random.normal(mu, sigma, num_traces)
        trace_lens = np.round(trace_lens)
        trace_lens = trace_lens[trace_lens > 1]
        c = collections.Counter(trace_lens)
        return c

    def __get_uniform_probabilities(self, num_probabilities: int):
        return [1 / num_probabilities for p in range(0, num_probabilities)]

    def __distribute_random_choices(self, min_num, max_num, traces_num, probabilities: [float]):
        prefixes = range(min_num, max_num + 1)
        trace_lens = np.random.choice(prefixes, traces_num, p=probabilities)
        c = collections.Counter(trace_lens)

        return c

    def distribution(
            self,
            min_num_events_or_mu: int,
            max_num_events_or_sigma: int,
            num_traces: int,
            dist_type: Literal["uniform", "normal", "custom"] = "uniform",
            custom_probabilities: Optional[List[float]] = None):
        if dist_type == "normal":
            return self.normal_distribution(min_num_events_or_mu, max_num_events_or_sigma, num_traces)
        elif dist_type == "uniform":
            return self.uniform_distribution(min_num_events_or_mu, max_num_events_or_sigma, num_traces)
        elif dist_type == "custom":
            return self.custom_distribution(min_num_events_or_mu, max_num_events_or_sigma, num_traces,
                                            custom_probabilities)
        else:
            raise AttributeError(f"Specified type of distribution {dist_type} not supported yet.")


if __name__ == "__main__":
    # print(distribution(2, 4, "uniform", num_traces=100))
    # print(normal_distribution(1.5, 0.15, 1000))
    # print(distribution(2, 10, "normal"))
    d = Distributor()
    print(d.uniform_distribution(2, 4, 10))
    print(d.custom_distribution(2, 4, 10, [0.3333333333333333, 0.3333333333333333, 0.3333333333333333]))
    print(d.normal_distribution(3, 4, 10))
