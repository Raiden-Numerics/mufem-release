import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("Table_1_BH_Curve.csv", delimiter=",", skiprows=1)

H = data[:, 1]
B = data[:, 0]

# Plot the BH curve
plt.plot(H, B, linewidth=2.5)

plt.xlabel("Magnetic Field Strength [A$\\,$m$^2$]")
plt.ylabel("Magnetic Flux Density [T]")

plt.xlim((0, 10000))
plt.ylim((0, 2.0))

plt.yticks([0.0, 0.5, 1.0, 1.5, 2.0])

plt.savefig("bh_curve.png", bbox_inches="tight")

plt.xlim((0, 1000))

plt.savefig("bh_curve_low.png", bbox_inches="tight")
