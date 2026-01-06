import matplotlib.pyplot as plt
import numpy as np


def to_db(value):
    # Use 20*log10 to convert amplitude to dB, not 10*log10 which is for power.
    level = np.max(value) * 1e-10
    value_lvl = np.copy(value)
    value_lvl[value_lvl < level] = level
    value_db = 20 * np.log10(value_lvl)
    return value_db - np.max(value_db)


# mufem results ------------------------------------------------------------------------
data = np.load("results/Far_Field_3D.npz")

thetas = data["thetas"]
phis = data["phis"]
radiation_pattern = data["radiation_pattern"]

thetas_full = np.concatenate((thetas, thetas + np.pi))

# E-plane:
iph = np.argmin(np.abs(phis - 0.0))
eplane = radiation_pattern[:, iph]
eplane = eplane / np.max(eplane)
eplane_full = np.concatenate((eplane, eplane[::-1]))

# H-plane:
ith = np.argmin(np.abs(thetas - np.pi / 2))
hplane = radiation_pattern[ith, :]
hplane = hplane / np.max(hplane)


# Analytic solution --------------------------------------------------------------------
# W.L. Stutzman "Antenna Theory and Design", 3rd ed., (2012), section 3.2
#
# Far-field radiation pattern:
#    E(θ,ϕ) = |cos(π/2 cos(θ)) / sin(θ)|

# E-plane (ϕ=0):
#    E(θ,ϕ=0) = |cos(π/2 cos(θ)) / sin(θ)|
eplane_theory = np.zeros(len(thetas))
for i, theta in enumerate(thetas):
    if np.sin(theta) > 1e-6:
        eplane_theory[i] = np.abs(np.cos(np.pi / 2 * np.cos(theta)) / np.sin(theta))
eplane_theory_full = np.concatenate((eplane_theory, eplane_theory[::-1]))


# H-plane (θ=π/2):
#    E(θ=π/2,ϕ) = 1
hplane_theory = np.ones(len(phis))


# Plot ---------------------------------------------------------------------------------
# E-plane:
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.plot(thetas_full, to_db(eplane_theory_full), "k-", label="Analytic")
ax.plot(thetas_full, to_db(eplane_full), "r-", label="$\\mu$fem")
ax.set_ylim(-12, 2)
ax.set_yticks([-10, -8, -6, -4, -2, 0])
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 0.12))
ax.set_title("E-plane", fontweight="bold")
plt.savefig("results/Far_Field_E-plane.png", bbox_inches="tight")

# H-plane:
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.plot(phis, to_db(hplane_theory), "k-", label="Analytic")
ax.plot(phis, to_db(hplane), "r-", label="$\\mu$fem")
ax.set_ylim(-12, 2)
ax.set_yticks([-10, -8, -6, -4, -2, 0])
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 0.12))
ax.set_title("H-plane", fontweight="bold")
plt.savefig("results/Far_Field_H-plane.png", bbox_inches="tight")

plt.show()
