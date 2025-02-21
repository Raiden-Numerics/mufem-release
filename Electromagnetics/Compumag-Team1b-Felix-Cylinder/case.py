import mufem

from mufem import Bnd, Vol
from mufem.electromagnetics.timedomainmagnetic import (
    TangentialMagneticFieldBoundaryCondition,
    TimeDomainMagneticGeneralMaterial,
    TimeDomainMagneticModel,
)

sim = mufem.Simulation.New(
    name="Compumag Team1b: Felix Cylinder", mesh_path="geometry.mesh"
)

# Setup Problem
mufem.UnsteadyRunner(total_time=0.02, time_step_size=0.001, total_inner_iterations=2)

magnetic_model = TimeDomainMagneticModel(
    marker=["Air", "Cylinder"] @ Vol, order=1, magnetostatic_initialization=True
)

# Setup Materials
air_material = TimeDomainMagneticGeneralMaterial.Vacuum(name="Air", marker="Air" @ Vol)

copper_material = TimeDomainMagneticGeneralMaterial.NonMagnetic(
    name="Al", marker="Cylinder" @ Vol, electric_conductivity=25380710.659898475
)
magnetic_model.add_materials([air_material, copper_material])

# Setup Boundary Conditions
cff_fall = mufem.CffExpressionScalar("79577.488101574*exp(-time()/0.0069)")
cff_zero = mufem.CffConstantScalar(0.0)

cff_magnetic_field = mufem.CffVectorComponent(
    cff_x=cff_zero, cff_y=cff_fall, cff_z=cff_zero
)

tangential_magnetic_field_bc = TangentialMagneticFieldBoundaryCondition(
    name="ExternalField",
    marker="Air::Boundary" @ Bnd,
    tangential_magnetic_field=cff_magnetic_field,
)
magnetic_model.add_condition(tangential_magnetic_field_bc)

# Setup Reports
ohmic_heating_report = mufem.VolumeIntegralReport(
    name="Ohmic Heating", marker="Cylinder" @ Vol, cff_name="OhmicHeating"
)
sim.get_report_manager().add_report(ohmic_heating_report)


ohmic_heating_monitor = mufem.ReportMonitor(
    name="Ohmic Heating Monitor", report_name="Ohmic Heating"
)
sim.get_monitor_manager().add_monitor(ohmic_heating_monitor)


sim.run()

# Plot the losses

# flake8: noqa

import pylab

monitor_values = ohmic_heating_monitor.get_values()


values = [(value[0], value[1]) for value in monitor_values]


pylab.clf()

power_loss_reference = pylab.loadtxt("data/PowerLoss.csv", delimiter=",")

pylab.plot(
    power_loss_reference[:, 0],
    power_loss_reference[:, 1],
    "k-",
    label="Davey et al.",
    linewidth=2.5,
    markersize=6.5,
)

pylab.plot(
    *zip(*values),
    "r.-",
    label="$\\mu$fem",
    markersize=6.5,
    linewidth=2.0,
)

pylab.xlabel("Time t [s]")
pylab.ylabel("Ohmic Heating Loss P$_\\Omega$ [W]")
pylab.xlim(0, 0.02)
pylab.xticks([0, 0.01, 0.02])
pylab.ylim(0, 600)
pylab.legend(loc="best").draw_frame(False)

pylab.savefig(f"OhmicHeating.png")
