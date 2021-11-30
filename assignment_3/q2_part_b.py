import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def calc_theta(degree_freq, Ik_u, Ik_v, rho, total_degree):
    theta = 0
    for k in range(len(degree_freq)):
            theta += (k*Ik_u[k]+ k*Ik_v[k]*(1-rho))/total_degree

    return theta


def sis_config_model(degree_sequence):
    # Graph Setup
    G = nx.configuration_model(degree_sequence)
    degree_freq = nx.degree_histogram(G)
    G_deg_sum = [a * b for a, b in zip(degree_freq, range(0, len(degree_freq)))]
    total_degree = sum(G_deg_sum)

    I0_u = 0
    I0_v = 0.01
    S0_u = 0.6*(1 - I0_v - I0_u)
    S0_v = 0.4*(1 - I0_v - I0_u)

    Sk_v = np.zeros((len(degree_freq)))
    Ik_v = np.zeros((len(degree_freq)))
    Sk_u = np.zeros((len(degree_freq)))
    Ik_u = np.zeros((len(degree_freq)))
    for k in range(len(degree_freq)):

        Ik_v[k] = degree_freq[k]*I0_v
        Ik_u[k] = degree_freq[k]*I0_u
        Sk_v[k] = degree_freq[k]*S0_v
        Sk_u[k] = degree_freq[k]*S0_u

    # SIS Set up
    beta = 0.3
    h = 0.1
    alpha = 1
    rho = 0.5
    history = []

    num_steps = 500
    T = np.arange(1, num_steps/h)
    S_u = np.zeros(len(T))
    I_u = np.zeros(len(T))
    S_v = np.zeros(len(T))
    I_v = np.zeros(len(T))

    S = np.zeros(len(T))
    I = np.zeros(len(T))

    S_u[0] = S0_u*len(degree_sequence)
    I_u[0] = I0_u*len(degree_sequence)
    S_v[0] = S0_v*len(degree_sequence)
    I_v[0] = I0_v*len(degree_sequence)

    S[0] = S_u[0] + S_v[0]
    I[0] = I_u[0] + I_v[0]

    # Run model
    for i in range(0, len(T)-1):

        theta = calc_theta(degree_freq, Ik_u, Ik_v, rho, total_degree)
        history.append(theta)
        sus = 0
        inf = 0

        sus_u = 0
        inf_u = 0
        sus_v = 0
        inf_v = 0
        for k in range(len(degree_freq)):
            delta_Sk_v = alpha*Ik_v[k] - (1-rho)*beta*k*theta*Sk_v[k]
            delta_Ik_v = (1-rho)*beta*k*theta*Sk_v[k] - alpha*Ik_v[k]
            delta_Sk_u = alpha*Ik_u[k] - beta*k*theta*Sk_u[k]
            delta_Ik_u = beta*k*theta*Sk_u[k] - alpha*Ik_u[k]


            Sk_v[k] += delta_Sk_v*h
            Ik_v[k] += delta_Ik_v*h
            Sk_u[k] += delta_Sk_u*h
            Ik_u[k] += delta_Ik_u*h

            sus += Sk_v[k] + Sk_u[k]
            inf += Ik_v[k] + Ik_u[k]

            sus_v += Sk_v[k]
            sus_u += Sk_u[k]
            inf_v += Ik_v[k]
            inf_u += Ik_u[k]

        S[i+1] = sus
        I[i+1] = inf

        S_u[i+1] = sus_u
        I_u[i+1] = inf_u
        S_v[i+1] = sus_v
        I_v[i+1] = inf_v

    fig,ax = plt.subplots()
    ax.plot(h*T, S_u, 'b', label='Susceptible_u')
    ax.plot(h*T,I_u, 'r', label='Infectious_u')
    ax.plot(h*T,S_v, 'g', label='Susceptible_v')
    ax.plot(h*T,I_v, 'y', label='Infectious_v')
    ax.legend()
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title("SIS Model")
    # plt.show()
    plt.savefig("q2_part_b_fig1.png")

def main():
    n = 1000
    p = 0.25
    sequence = np.random.geometric(p,size=n)
    if sum(sequence) % 2 != 0:
        sequence[0] +=1
    sis_config_model(sequence)

if __name__ == '__main__':
    main()