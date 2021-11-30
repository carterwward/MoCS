import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def calc_theta(degree_freq, Ik_u, Ik_v, rho, total_degree):
    theta = 0
    for k in range(len(degree_freq)):
            theta += (k*Ik_u[k] + k*Ik_v[k]*(1-rho))/total_degree

    return theta

def sis_config_model(degree_sequence, rho, axs, plot_num):
   # Graph Setup
    G = nx.configuration_model(degree_sequence)
    degree_freq = nx.degree_histogram(G)
    G_deg_sum = [a * b for a, b in zip(degree_freq, range(0, len(degree_freq)))]
    total_degree = sum(G_deg_sum)

    I0 = 0.01
    S0 = 1 - I0

    U0 = 0.6
    V0 = 0.4

    Sk_v = np.zeros(len(degree_freq))
    Ik_v = np.zeros(len(degree_freq))
    Sk_u = np.zeros(len(degree_freq))
    Ik_u = np.zeros(len(degree_freq))

    perc_array = np.cumsum(degree_freq)/len(degree_sequence)
    idx = (np.abs(perc_array - U0)).argmin()

    for k in range(idx+1):
        Ik_u[k] = degree_freq[k]*I0
        Sk_u[k] = degree_freq[k]*S0

    for k in range(idx+1, len(degree_freq)):
        Ik_v[k] = degree_freq[k]*I0
        Sk_v[k] = degree_freq[k]*S0

    # SIS Set up
    beta = 0.3
    h = 0.1
    alpha = 1
    history = []

    num_steps = 500
    T = np.arange(1,num_steps/h)

    S_u = np.zeros(len(T))
    I_u = np.zeros(len(T))
    S_v = np.zeros(len(T))
    I_v = np.zeros(len(T))

    S = np.zeros(len(T))
    I = np.zeros(len(T))

    S_u[0] = S0*U0*len(degree_sequence)
    I_u[0] = I0*U0*len(degree_sequence)
    S_v[0] = S0*V0*len(degree_sequence)
    I_v[0] = I0*V0*len(degree_sequence)

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
            delta_Sk_v = alpha*Ik_v[k] - beta*k*theta*Sk_v[k]
            delta_Ik_v = beta*k*theta*Sk_v[k] - alpha*Ik_v[k]

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
    axs[plot_num].plot(h*T, S_u, 'b', label='Susceptible_u')
    axs[plot_num].plot(h*T,I_u, 'r', label='Infectious_u')
    axs[plot_num].plot(h*T,S_v, 'g', label='Susceptible_v')
    axs[plot_num].plot(h*T,I_v, 'y', label='Infectious_v')
    axs[plot_num].set_title("rho = "+ str(rho))


def main():
    n = 1000
    p = 0.25
    sequence = np.random.geometric(p,size=n)
    rhos = [1.0, 0.75, 0.5, 0.25]
    if sum(sequence) % 2 != 0:
        sequence[0] +=1
    fig, axs = plt.subplots(ncols=2, nrows=2, sharex=True, sharey=True)
    axs = axs.ravel()
    for i, rho in enumerate(rhos):
        sis_config_model(sequence, rho, axs, i)

    fig.tight_layout()
    plt.legend()
    fig.text(0.02, 0.5, 'Time', ha='center', va='center', rotation='vertical')
    fig.text(0.5, 0.02, 'Population', ha='center', va='center')
    fig.text(0.5, .96, 'SIS Model', ha='center', va='center')
    fig.savefig("q2_part_d_fig1.png")

if __name__ == '__main__':
    main()