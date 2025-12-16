import matplotlib.pyplot as plt
import numpy as np

import mufem
from mufem import Bnd, Vol
from mufem.electromagnetics.timeharmonicmaxwell import (
    AbsorbingBoundaryCondition,
    FarFieldRadiationSensor,
    LumpedPortCondition,
    PerfectElectricConductorCondition,
    TimeHarmonicMaxwellGeneralMaterial,
    TimeHarmonicMaxwellModel,
)


# **************************************************************************************
# Problem setup
# **************************************************************************************
sim = mufem.Simulation.New(
    name="Stutzman 2012: Dipole Antenna", mesh_path="geometry.msh",
)

runner = mufem.SteadyRunner(total_iterations=1)
sim.set_runner(runner)


# **************************************************************************************
# Model
# **************************************************************************************
model = TimeHarmonicMaxwellModel(
    marker="Domain" @ Vol,
    frequency=0.0749e9,  # [Hz]
    order=2,  # finite element polynomial degree
)
sim.get_model_manager().add_model(model)


# **************************************************************************************
# Materials
# **************************************************************************************
material_air = TimeHarmonicMaxwellGeneralMaterial.Constant(
    name="Air", marker="Domain" @ Vol,
)
model.add_material(material_air)


# **************************************************************************************
# Boundary conditions
# **************************************************************************************
condition_outer = AbsorbingBoundaryCondition(
    name="AirBoundary", marker="BoundaryOuter" @ Bnd
)

condition_arms = PerfectElectricConductorCondition(
    name="PEC",  marker=["BoundaryTopArm", "BoundaryBotArm"] @ Bnd,
)

w = 0.10  # [m] port width
l = 0.04  # [m] port length
R = 50  # [Ohm] transmission line resistance
Z = R  # [Ohm] transmission line impedance: 1/Z = 1/R + 1/(i*w*L) + i*w*C
Zs = Z * w / l  # [Ohm] surface impedance
condition_port = LumpedPortCondition(
    name="Port",
    marker="Port" @ Bnd,
    surface_impedance=Zs,
    incident_electric_field_vector=(0, 0, 1),
)

model.add_conditions([condition_outer, condition_arms, condition_port])


# **************************************************************************************
# Run the simulation
# **************************************************************************************
sim.run()

# Export ParaView data:
vis = sim.get_field_exporter()
vis.add_field_output("Electric Field-Real")
vis.save(order=2)


# **************************************************************************************
# Plot E-plane and H-plane far-field radiation patterns
# **************************************************************************************
if sim.get_machine().is_main_process():
    print("\nPlot E-plane and H-plane far-field radiation patterns...")


# Analytic solution --------------------------------------------------------------------
# E-plane:
data = np.loadtxt("data/E-plane_Analytic.csv", delimiter=",")
thetas_theory = data[:, 0]
eplane_theory = data[:, 1]

# H-plane:
data = np.loadtxt("data/H-plane_Analytic.csv", delimiter=",")
phis_theory = data[:, 0]
hplane_theory = data[:, 1]


# mufem results ------------------------------------------------------------------------
# E-plane:
sensor = FarFieldRadiationSensor(
    "FarFieldRadiationSensor",
    polar_start=0.0,
    polar_stop=180.0,
    polar_step=6.0,
    azimuthal_start=0.0,
    azimuthal_stop=0.0,
    azimuthal_step=0.0,
)
thetas = np.array(sensor.get_polar_angles())
eplane = np.array(sensor.get_radiation_pattern())

eplane = eplane[:, 0] / np.max(eplane[:, 0])
thetas = np.concatenate((thetas, thetas + np.pi))
eplane = np.concatenate((eplane, eplane[::-1]))

# H-plane:
sensor = FarFieldRadiationSensor(
    "FarFieldRadiationSensor",
    polar_start=90.0,
    polar_stop=90.0,
    polar_step=0.0,
    azimuthal_start=0.0,
    azimuthal_stop=360.0,
    azimuthal_step=6.0,
)
phis = np.array(sensor.get_azimuthal_angles())
hplane = np.array(sensor.get_radiation_pattern())

hplane = hplane[0, :] / np.max(hplane[0, :])


# Plot ---------------------------------------------------------------------------------
# E-plane:
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.plot(thetas_theory, eplane_theory, "k-", label="Analytic")
ax.plot(thetas, eplane, "r-", label="$\\mu$fem")
ax.set_rmax(1.1)
ax.legend(loc=0)
plt.savefig("results/Far_Field_E-plane.png", bbox_inches="tight")

# H-plane:
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.plot(phis_theory, hplane_theory, "k-", label="Analytic")
ax.plot(phis, hplane, "r-", label="$\\mu$fem")
ax.set_rmax(1.1)
ax.legend(loc=0)
plt.savefig("results/Far_Field_H-plane.png", bbox_inches="tight")


# **************************************************************************************
# Export 3D far-field radiation pattern
# **************************************************************************************
if sim.get_machine().is_main_process():
    print("\nExport 3D far-field radiation pattern...")

sensor = FarFieldRadiationSensor(
    "FarFieldRadiationSensor",
    polar_start=0.0,
    polar_stop=180.0,
    polar_step=6.0,
    azimuthal_start=0.0,
    azimuthal_stop=360.0,
    azimuthal_step=6.0,
)
thetas = np.array(sensor.get_polar_angles())
phis = np.array(sensor.get_azimuthal_angles())
radiation_pattern = np.array(sensor.get_radiation_pattern())
radiation_pattern = radiation_pattern / np.max(radiation_pattern)

np.savez(
    "results/Far_Field_3D.npz",
    thetas=thetas,
    phis=phis,
    radiation_pattern=radiation_pattern,
)
