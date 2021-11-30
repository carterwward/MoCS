import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def calc_theta(degree_freq, Ik, total_degree):
    theta = 0
    for k in range(len(degree_freq)):
            theta += k*Ik[k]/total_degree

    return theta

def sis_config_model(degree_sequence):
    # Graph Setup
    G = nx.configuration_model(degree_sequence)
    degree_freq = nx.degree_histogram(G)
    G_deg_sum = [a * b for a, b in zip(degree_freq, range(0, len(degree_freq)))]
    total_degree = sum(G_deg_sum)

    Sk = np.zeros((len(degree_freq)))
    Ik = np.zeros((len(degree_freq)))
    I0 = 0.01
    S0 = 1.0 - I0
    for k in range(len(degree_freq)):
        Sk[k] = degree_freq[k]*S0
        Ik[k] = degree_freq[k]*I0

    # SIS Set up
    beta = 0.3
    h = 0.1
    alpha = 1
    num_steps = 500
    T = np.arange(1,num_steps/h)
    S = np.zeros(len(T))
    I = np.zeros(len(T))

    S[0] = S0*len(degree_sequence)
    I[0] = I0*len(degree_sequence)

    # Run model
    for i in range(0, len(T)-1):
        theta = calc_theta(degree_freq, Ik, total_degree)
        sus = 0
        inf = 0
        for k in range(len(degree_freq)):
            delta_Sk = alpha*Ik[k]-beta*k*theta*Sk[k]
            delta_Ik = beta*k*theta*Sk[k] - alpha*Ik[k]
            Sk[k] += delta_Sk*h
            Ik[k] += delta_Ik*h

            sus += Sk[k]
            inf += Ik[k]
        S[i+1] = sus
        I[i+1] = inf

    plt.plot(h*T,S, label="Susceptible")
    plt.plot(h*T, I, label="Infected")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title("SIS Model")
    plt.show()
    plt.savefig("q2_part_a_fig1.png")

def main():
    n = 1000
    p = 0.25
    sequence = np.random.geometric(p,size=n)
    if sum(sequence) % 2 != 0:
        sequence[0] +=1
    sis_config_model(sequence)

if __name__ == '__main__':
    main()
