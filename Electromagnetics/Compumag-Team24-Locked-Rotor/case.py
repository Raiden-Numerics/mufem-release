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


sim = mufem.Simulation.New("Team-24", "geometry.mesh")

is_main_process = sim.getMachine().isMainProcess()


unsteady_runner = mufem.UnsteadyRunner(
    total_time=0.15, time_step_size=0.005, total_inner_iterations=6
)
sim.setRunner(unsteady_runner)


magnetic_domain = ["Rotor", "Stator", "Upper Coil", "Lower Coil", "Air"] @ Vol

magnetic_model = TimeDomainMagneticModel(magnetic_domain, 1, False)
sim.getModelManager().addModel(magnetic_model)


# Define the materials
air_material = TimeDomainMagneticGeneralMaterial.SimpleVacuum("Air", "Air" @ Vol)

copper_material = TimeDomainMagneticGeneralMaterial.SimpleNonMagnetic(
    "Copper", ["Upper Coil", "Lower Coil"] @ Vol, 5.8e7
)
copper_material.setEddyCurrents(False)

bh = numpy.loadtxt(f"tables/Updated_BH_curve.csv", delimiter=",", comments="#")


iron_material = TimeDomainMagneticGeneralMaterial.SimpleNonLinear(
    "Iron", ["Rotor", "Stator"] @ Vol, bh[:, 0], bh[:, 1], 4.54e6
)

magnetic_model.addMaterials([air_material, copper_material, iron_material])

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
    "TangentialFlux", boundary_marker
)
magnetic_model.addCondition(tangential_magnetic_flux_bc)

# Setup Coil
coil_model = ExcitationCoilModel()
sim.getModelManager().addModel(coil_model)

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
        f"{coil} Coil::In" @ Bnd, f"{coil} Coil::Out" @ Bnd
    )

    coil = CoilSpecification(
        f"{coil} Coil",
        f"{coil} Coil" @ Vol,
        coil_topology,
        coil_type,
        coil_excitation,
    )
    coil_model.addCoilSpecification(coil)


# Setup Reports
magnetic_torque_report = MagneticTorqueReport("Rotor Torque", "Rotor" @ Vol)
sim.getReportManager().addReport(magnetic_torque_report)

magnetic_torque_monitor = mufem.ReportMonitor("Rotor Torque Monitor", "Rotor Torque")
sim.getMonitorManager().addMonitor(magnetic_torque_monitor)


sim.run()

# After the simulation has run, we plot the results
import pylab

symmetry_factor = 2.0

monitor_values = magnetic_torque_monitor.getValues()

values = [
    (value[0], symmetry_factor * value[1].getVectorValue().z)
    for value in monitor_values
]


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
