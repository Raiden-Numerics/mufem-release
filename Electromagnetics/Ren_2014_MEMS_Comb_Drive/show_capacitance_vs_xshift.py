import matplotlib.pyplot as plt
import numpy as np

xshifts = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]

N = len(xshifts)

x = np.zeros(N)
C = np.zeros(N)

for i, xshift in enumerate(xshifts):
    fname = f"results/Capacitance_xshift={xshift:.1f}.csv"

    data = np.loadtxt(fname, delimiter=",")
    dofs = data[:, 0]
    capacitance = data[:, 1]

    x[i] = float(fname.split('_')[-1][:-4].split('=')[-1]) * 1e-6
    C[i] = capacitance[-1]

a, b = np.polyfit(x, C, 1)
print(a, " ", b)

V = 1  # [V] applied voltage
dCdx = a   # [F/m] derivative of the capacitance
F = 1/2 * dCdx * V**2  # [N] comb drive force

print(f"Force F = {F} [N]")
print(f"Force F = {F/1e-9} [nN]")

plt.figure(constrained_layout=True)
plt.plot(x / 1e-6, C / 1e-15, "o", label="$\\mu$fem")
plt.plot(x / 1e-6, (a * x + b) / 1e-15, "-", label="linear fit")
plt.legend(loc=0, frameon=False)
plt.xlabel("Shift [$\mu$m]")
plt.ylabel("Capacitance [fF]")
plt.savefig("results/Capacitance_Vs_Xshift.png")

plt.show()