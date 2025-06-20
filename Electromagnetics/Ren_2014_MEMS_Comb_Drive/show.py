import matplotlib.pyplot as plt
import numpy as np


fnames = [
    "results/Capacitance_0.csv",
    "results/Capacitance_1.csv",
    "results/Capacitance_2.csv",
]


plt.figure(constrained_layout=True)

for i, fname in enumerate(fnames):
    data = np.loadtxt(fname, delimiter=",")

    dofs = data[:, 0]
    capacitance = data[:, 1]

    plt.plot(dofs / 1e-3, capacitance / 1e-15, "o-", label=f"geometry_{i}.msh")

plt.legend(loc=0)
plt.xlabel("Number of degrees of freedom [10³]")
plt.ylabel("Capacitance [fF]")
plt.savefig("results/Capacitance.png")

plt.show()