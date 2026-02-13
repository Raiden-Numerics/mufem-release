import matplotlib.pyplot as plt
import numpy

import mufem
from mufem import Bnd, Vol
from mufem.thermal import (
    AdiabaticBoundaryCondition,
    ConvectionBoundaryCondition,
    SolidTemperatureMaterial,
    SolidTemperatureModel,
    TemperatureCondition,
)

# Problem setup ------------------------------------------------------------------------
sim = mufem.Simulation.New(
    name="Cameron 1986: Heat Transfer With Convection",
    mesh_path="geometry.mesh",
)

runner = mufem.SteadyRunner(total_iterations=3)
sim.set_runner(runner)

is_main_process = sim.get_machine().is_main_process()

# Model --------------------------------------------------------------------------------
model = SolidTemperatureModel(marker="Plate" @ Vol)
sim.get_model_manager().add_model(model)

# Materials ----------------------------------------------------------------------------
material = SolidTemperatureMaterial(
    name="Material",
    marker="Plate" @ Vol,
    thermal_conductivity=52.0,
    specific_heat_capacity=1.0,
    density=1.0,
)
model.add_material(material)

# Boundary conditions ------------------------------------------------------------------
bc_Adiabatic = AdiabaticBoundaryCondition(
    name="Insulated",
    marker="Plate::Insulated" @ Bnd,
)

bc_TAmbient = ConvectionBoundaryCondition(
    name="Natural Convection",
    marker="Plate::AmbientTemperature" @ Bnd,
    convection_efficiency=750.0,
    temperature_medium=273.15,
)

bc_TFixed = TemperatureCondition(
    name="Fixed Temperature",
    marker="Plate::FixedTemperature" @ Bnd,
    temperature=373.15,
)

model.add_conditions([bc_TFixed, bc_TAmbient, bc_Adiabatic])

# Run the simulation -------------------------------------------------------------------
sim.run()

# Test the temperature -----------------------------------------------------------------
report = mufem.ProbeReport.SinglePoint(
    name="TemperatureReport",
    cff_name="Temperature",
    x=0.6,
    y=0.2,
    z=0.005,
)
Tprobe = report.evaluate()

Texpected = 291.45

if is_main_process:
    print()
    print(f"Expected temperature T = {Texpected} K")
    print(f"   Probe Temperature T = {Tprobe} K")
    print()

# Plot the temperature -----------------------------------------------------------------
eps = 1.0e-6
x_vals = numpy.linspace(0, 0.6, 23, endpoint=True)
T_vals = []

for x in x_vals:
    report = mufem.ProbeReport.SinglePoint(
        name="Probe Report",
        cff_name="Temperature",
        x=x,
        y=0.5,
        z=0.005,
    )
    T_vals.append(report.evaluate())

plt.plot(x_vals, T_vals, color="red")
plt.xlabel("Position [m]")
plt.ylabel("Temperature [K]")
plt.savefig("results/Temperature.png", bbox_inches="tight")

# Export ParaView data -----------------------------------------------------------------
vis = sim.get_field_exporter()
vis.add_field_output("Temperature")
vis.save()
