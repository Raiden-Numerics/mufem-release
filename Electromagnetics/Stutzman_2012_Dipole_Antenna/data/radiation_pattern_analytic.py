import os
import numpy as np
import matplotlib.pyplot as plt

# W.L. Stutzman "Antenna Theory and Design", 3rd ed., (2012), section 3.2
#
# Far-field radiation pattern:
#    E(θ,ϕ) = |cos(π/2 cos(θ)) / sin(θ)|

# E-plane (ϕ=0):
#    E(θ,ϕ=0) = |cos(π/2 cos(θ)) / sin(θ)|
thetas = np.linspace(0, np.pi, 180)
eplane = np.zeros(len(thetas))
for i, theta in enumerate(thetas):
    if np.sin(theta) > 1e-6:
        eplane[i] = np.abs(np.cos(np.pi / 2 * np.cos(theta)) / np.sin(theta))
thetas = np.concatenate((thetas, thetas + np.pi))
eplane = np.concatenate((eplane, eplane[::-1]))

# H-plane (θ=π/2):
#    E(θ=π/2,ϕ) = 1
phis = np.linspace(0, 2 * np.pi, 360)
hplane = np.ones(len(phis))

header = "Polar angle [rad], E-plane far-field radiation pattern [V]"
data = np.column_stack((thetas, eplane))
np.savetxt(
    os.path.join(os.path.dirname(__file__), "E-plane_Analytic.csv"),
    data,
    delimiter=", ",
    comments="# ",
    header=header,
)

header = "Azimuthal angle [rad], H-plane far-field radiation pattern [V]"
data = np.column_stack((phis, hplane))
np.savetxt(
    os.path.join(os.path.dirname(__file__), "H-plane_Analytic.csv"),
    data,
    delimiter=", ",
    comments="# ",
    header=header,
)

fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.plot(thetas, eplane, "k-", label="Analytic")
ax.set_rmax(1.1)
ax.legend(loc=0)

fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.plot(phis, hplane, "k-", label="Analytic")
ax.set_rmax(1.1)
ax.legend(loc=0)

plt.show()
