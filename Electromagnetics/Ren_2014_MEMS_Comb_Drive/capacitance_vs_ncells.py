import matplotlib.pyplot as plt
import numpy as np

xshifts = [0, 2, 4, 6, 8]

data = np.loadtxt("results/Capacitance.csv", delimiter=",")

plt.figure(constrained_layout=True)

for i, xshift in enumerate(xshifts):
    subdata = data[data[:, 0] == xshift]

    ncells = subdata[:, 1]
    capacitance = subdata[:, 2]

    plt.plot(ncells / 1e3, capacitance / 1e-15, "o-", label=f"xshift = {xshift:.1f} μm")

plt.ylim(2, 6)
plt.legend(loc=0, frameon=False)
plt.xlabel("Number of cells [10³]")
plt.ylabel("Capacitance [fF]")
plt.savefig("results/Capacitance_Vs_Ncells.png")

plt.show()
