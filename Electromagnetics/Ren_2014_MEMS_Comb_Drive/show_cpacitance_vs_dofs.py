import matplotlib.pyplot as plt
import numpy as np

# xshifts = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
xshifts = [0, 2, 4, 6, 8]

plt.figure(constrained_layout=True)

for i, xshift in enumerate(xshifts):
    fname = f"results/Capacitance_xshift={xshift:.1f}.csv"

    data = np.loadtxt(fname, delimiter=",")

    dofs = data[:, 0]
    capacitance = data[:, 1]

    label = fname.split('_')[-1][:-4]

    plt.plot(dofs / 1e3, capacitance / 1e-15, "o-", label=label)

plt.legend(loc=0, frameon=False)
plt.xlabel("Number of degrees of freedom [10³]")
plt.ylabel("Capacitance [fF]")
plt.savefig("results/Capacitance_Vs_Dofs.png")

plt.show()