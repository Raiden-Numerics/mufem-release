import numpy

from mufem import (
    Bnd, Vol, SteadyRunner, CffConstantScalar, Simulation
)
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


sim = Simulation.New("Compumag-Team20-3D-Static-Force-Problem", "geometry.mesh")


# Setup Problem
steady_runner = SteadyRunner(total_iterations=0)

magnetic_domain = ["Yoke", "Pole", "Coil", "Air"] @ Vol
magnetic_model = TimeDomainMagneticModel(magnetic_domain, 1, False)

air_material = TimeDomainMagneticGeneralMaterial.SimpleVacuum("Air", "Air" @ Vol)
copper_material = TimeDomainMagneticGeneralMaterial.SimpleNonMagnetic(
    "Copper", "Coil" @ Vol, 1.0e7
)

bh = numpy.loadtxt("data/Table_1_BH_Curve.csv", delimiter=",", skiprows=1)

iron_material = TimeDomainMagneticGeneralMaterial.SimpleNonLinear(
    "Iron", ["Yoke", "Pole"] @ Vol, bh[:, 1], bh[:, 0], 0.0
)

magnetic_model.addMaterials([air_material, copper_material, iron_material])

# Boundaries
tangential_magnetic_flux_bc = TangentialMagneticFluxBoundaryCondition(
    "TangentialFlux",
    [
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

coil_topology = CoilTopologyOpen("Coil::In" @ Bnd, "Coil::Out" @ Bnd)
coil_type = CoilTypeStranded(1000)

coil_drive_current = CffConstantScalar(1.0)
coil_excitation = CoilExcitationCurrent(coil_drive_current)

coil = CoilSpecification(
    "Coil", "Coil" @ Vol, coil_topology, coil_type, coil_excitation
)
coil_model.addCoilSpecification(coil)


magnetic_force_report_1 = MagneticForceReport("Pole Force", "Pole" @ Vol)


# Run the scan

center_piece_force_list: List[float] = []

for coil_current in numpy.linspace(0.0, 5.0, 11):

    coil_drive_current.setValue(coil_current)

    steady_runner.advance(5)

    force_z = magnetic_force_report_1.evaluate()[0].getVectorValue().to_tuple()[2]

    center_piece_force_list.append((coil_current, force_z))


# Plot the results


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
