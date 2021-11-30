import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from itertools import count


def voter_model(graph, rho, timesteps, iterations):
    for node in graph.nodes:
        prob = np.random.uniform(0, 1)

        if prob > rho:
            graph.nodes[node]['color'] = 'red'
        else:
            graph.nodes[node]['color'] = 'blue'

    experiments = [deepcopy(graph) for i in range(iterations)]
    out = []
    timeseries_data = {}

    for experiment in experiments:
        experiment_ts = {'red': [], 'blue': [], 'step': []}
        for i in range(timesteps):
            num_red = 0
            num_blue = 0
            experiment_ts['step'].append(i)

            for node in experiment.nodes:
                if experiment.nodes[node]['color'] == 'red':
                    num_red += 1
                else:
                    num_blue += 1
            experiment_ts['red'].append(num_red)
            experiment_ts['blue'].append(num_blue)

            node = np.random.choice(experiment.nodes)
            neighbor = np.random.choice([neighbor for neighbor in experiment.neighbors(node)])
            experiment.nodes[node]['color'] = experiment.nodes[neighbor]['color']

        out.append(experiment)
        timeseries_data[experiment] = experiment_ts

    return out, timeseries_data


G = nx.karate_club_graph()  # or some graph of your choice!

experiments, timeseries = voter_model(G, 0.4, 50, 5)

for experiment in experiments:
    ts_data = timeseries[experiment]
    groups = set(nx.get_node_attributes(experiment, 'color').values())
    mapping = dict(zip(sorted(groups), count()))
    colors = [mapping[experiment.nodes[n]['color']] for n in experiment.nodes]
    nx.draw(experiment, node_color=colors)
    plt.show()

    plt.plot(ts_data['step'], ts_data['red'], color='red')
    plt.plot(ts_data['step'], ts_data['blue'], color='blue')
    plt.legend(['red', 'blue'], loc='upper left')
    plt.show()