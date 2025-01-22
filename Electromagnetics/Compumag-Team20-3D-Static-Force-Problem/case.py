import numpy

from mufem import Bnd, Vol, SteadyRunner, CffConstantScalar, Simulation
from mufem.electromagnetics.coil import (
    CoilExcitationCurrent,
    CoilSpecification,
    CoilTopologyOpen,
    CoilTypeStranded,
    ExcitationCoilModel,
)
from mufem.electromagnetics.timedomainmagnetic import (
    MagneticForceReport,
    TangentialMagneticFluxBoundaryCondition,
    TimeDomainMagneticGeneralMaterial,
    TimeDomainMagneticModel,
)

from typing import List


sim = Simulation.New(
    name="Compumag-Team20-3D-Static-Force-Problem", mesh_path="geometry.mesh"
)


# Setup Problem
steady_runner = SteadyRunner(total_iterations=0)

magnetic_domain = ["Yoke", "Pole", "Coil", "Air"] @ Vol
magnetic_model = TimeDomainMagneticModel(marker=magnetic_domain, order=1)

air_material = TimeDomainMagneticGeneralMaterial.SimpleVacuum(
    name="Air", marker="Air" @ Vol
)
copper_material = TimeDomainMagneticGeneralMaterial.SimpleNonMagnetic(
    name="Copper", marker="Coil" @ Vol, electric_conductivity=1.0e7
)

bh = numpy.loadtxt("data/Table_1_BH_Curve.csv", delimiter=",", comments="#")

iron_material = TimeDomainMagneticGeneralMaterial.SimpleNonLinear(
    name="Iron",
    marker=["Yoke", "Pole"] @ Vol,
    magnetic_field_strength=bh[:, 1],
    magnetic_flux_density=bh[:, 0],
    electric_conductivity=0.0,
)

magnetic_model.addMaterials([air_material, copper_material, iron_material])

# Boundaries
tangential_magnetic_flux_bc = TangentialMagneticFluxBoundaryCondition(
    name="TangentialFlux",
    marker=[
        "Yoke::PerfectElectric",
        "Pole::PerfectElectric",
        "Coil::In",
        "Coil::Out",
        "Air::PerfectElectric",
    ]
    @ Bnd,
)
magnetic_model.addCondition(tangential_magnetic_flux_bc)

# Coil
coil_model = ExcitationCoilModel()
sim.getModelManager().addModel(coil_model)

coil_topology = CoilTopologyOpen(
    in_marker="Coil::In" @ Bnd, out_marker="Coil::Out" @ Bnd
)
coil_type = CoilTypeStranded(number_of_turns=1000)

coil_drive_current = CffConstantScalar(1.0)
coil_excitation = CoilExcitationCurrent(coil_drive_current)

coil = CoilSpecification(
    name="Coil",
    marker="Coil" @ Vol,
    topology=coil_topology,
    type=coil_type,
    excitation=coil_excitation,
)
coil_model.addCoilSpecification(coil)

magnetic_force_report_1 = MagneticForceReport(name="Pole Force", marker="Pole" @ Vol)


# Run the scan

center_piece_force_list: List[float] = []

for coil_current in numpy.linspace(0.0, 5.0, 11):

    coil_drive_current.setValue(coil_current)

    steady_runner.advance(5)

    force_z = magnetic_force_report_1.evaluate()[0].getVectorValue().to_tuple()[2]

    center_piece_force_list.append((coil_current, force_z))


# Plot the results
# flake8: noqa

import pylab

pylab.clf()

symmetry_factor = 4.0

calculated = numpy.array(center_piece_force_list)

reference = numpy.loadtxt("data/ReferenceForce.csv", delimiter=",", comments="#")

pylab.plot(reference[:, 0], reference[:, 1], "ko", label="Reference")

pylab.plot(
    calculated[:, 0],
    symmetry_factor * calculated[:, 1],
    "r-",
    linewidth=2.5,
    label="$\\mu$fem",
)

pylab.xlabel("Coil Current [A]")
pylab.ylabel("Pole Force [N]")

pylab.legend(loc="best").draw_frame(False)

pylab.xlim(0.0, 5.4)
pylab.ylim(0, 90)

pylab.savefig(
    f"Force_vs_Current.png",
    bbox_inches="tight",
)
