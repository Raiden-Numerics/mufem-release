import mufem
import numpy

from mufem import Bnd, Vol

from mufem.electromagnetics.coil import (
    CoilExcitationCurrent,
    CoilSpecification,
    CoilTopologyOpen,
    CoilTypeStranded,
    ExcitationCoilModel,
)
from mufem.electromagnetics.timedomainmagnetic import (
    MagneticTorqueReport,
    TangentialMagneticFluxBoundaryCondition,
    TimeDomainMagneticGeneralMaterial,
    TimeDomainMagneticModel,
)


sim = mufem.Simulation.New(name="Team-24", mesh_path="geometry.mesh")

unsteady_runner = mufem.UnsteadyRunner(
    total_time=0.15, time_step_size=0.005, total_inner_iterations=6
)
sim.set_runner(unsteady_runner)


magnetic_domain = ["Rotor", "Stator", "Upper Coil", "Lower Coil", "Air"] @ Vol

magnetic_model = TimeDomainMagneticModel(marker=magnetic_domain, order=1)
sim.get_model_manager().add_model(magnetic_model)


# Define the materials
air_material = TimeDomainMagneticGeneralMaterial.Vacuum(name="Air", marker="Air" @ Vol)

copper_material = TimeDomainMagneticGeneralMaterial.NonMagnetic(
    name="Copper",
    marker=["Upper Coil", "Lower Coil"] @ Vol,
    electric_conductivity=5.8e7,
)
copper_material.set_eddy_currents(False)

bh = numpy.loadtxt(f"tables/Updated_BH_curve.csv", delimiter=",", comments="#")


iron_material = TimeDomainMagneticGeneralMaterial.MagneticNonLinear(
    name="Iron",
    marker=["Rotor", "Stator"] @ Vol,
    magnetic_field_strength=bh[:, 0],
    magnetic_flux_density=bh[:, 1],
    electric_conductivity=4.54e6,
)

magnetic_model.add_materials([air_material, copper_material, iron_material])

# Setup Boundaries
boundary_marker = [
    "Stator::1::TangentialFlux",
    "Rotor::1::TangentialFlux",
    "Air::TangentialFlux",
    "Upper Coil::In",
    "Upper Coil::Out",
    "Lower Coil::In",
    "Lower Coil::Out",
] @ Bnd

tangential_magnetic_flux_bc = TangentialMagneticFluxBoundaryCondition(
    name="TangentialFlux", marker=boundary_marker
)
magnetic_model.add_condition(tangential_magnetic_flux_bc)

# Setup Coil
coil_model = ExcitationCoilModel()
sim.get_model_manager().add_model(coil_model)

coil_type = CoilTypeStranded(350)

current_time = numpy.loadtxt(
    f"tables/Table_3_Coil_Current.csv",
    delimiter=",",
    comments="#",
)

coil_drive_current = mufem.CffTimeTable(current_time[:, 0], current_time[:, 1])

coil_excitation = CoilExcitationCurrent(coil_drive_current)


for coil in ["Upper", "Lower"]:

    coil_topology = CoilTopologyOpen(
        in_marker=f"{coil} Coil::In" @ Bnd, out_marker=f"{coil} Coil::Out" @ Bnd
    )

    coil = CoilSpecification(
        name=f"{coil} Coil",
        marker=f"{coil} Coil" @ Vol,
        topology=coil_topology,
        type=coil_type,
        excitation=coil_excitation,
    )
    coil_model.add_coil_specification(coil)


# Setup Reports
magnetic_torque_report = MagneticTorqueReport(name="Rotor Torque", marker="Rotor" @ Vol)
sim.get_report_manager().add_report(magnetic_torque_report)

magnetic_torque_monitor = mufem.ReportMonitor(
    name="Rotor Torque Monitor", report_name="Rotor Torque"
)
sim.get_monitor_manager().add_monitor(magnetic_torque_monitor)


sim.run()

# After the simulation has run, we plot the results

# flake8: noqa

import pylab

symmetry_factor = 2.0

monitor_values = magnetic_torque_monitor.getValues()

values = [(value[0], symmetry_factor * value[1].z) for value in monitor_values]


torque_ref = numpy.loadtxt(f"tables/Table_4_Torque.csv", delimiter=",", skiprows=1)

pylab.plot(torque_ref[:, 0], torque_ref[:, 1], "k-", label="Reference")
pylab.plot(*zip(*values), "r.-", label="$\\mu$fem")

pylab.xlim((0, 0.15))
pylab.ylim((0.0, 3.5))

pylab.xticks([0.0, 0.05, 0.1, 0.15])


pylab.xlabel("Time t [s]")
pylab.ylabel("Torque T [Nm]")

pylab.legend(loc="best").draw_frame(False)


pylab.savefig(f"Time_vs_Rotor_Torque.png", bbox_inches="tight")
