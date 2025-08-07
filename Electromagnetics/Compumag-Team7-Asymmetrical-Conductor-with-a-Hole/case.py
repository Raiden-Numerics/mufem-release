import mufem
from mufem.electromagnetics.coil import (
    CoilExcitationCurrent,
    CoilSpecification,
    CoilTopologyClosed,
    CoilTypeStranded,
    ExcitationCoilModel,
)
from mufem.electromagnetics.timeharmonicmagnetic import (
    TimeHarmonicMagneticGeneralMaterial,
    TimeHarmonicMagneticModel,
)

from mufem import Vol

import matplotlib.pyplot as plt
import numpy
from pathlib import Path

import mufem


dir_path = Path(__file__).resolve().parent


sim = mufem.Simulation.New(name="Team-7", mesh_path=f"{dir_path}/geometry.mesh")

# Setup Problem
steady_runner = mufem.SteadyRunner(total_iterations=1)
sim.set_runner(steady_runner)

magnetic_model = TimeHarmonicMagneticModel(Vol.Everywhere, frequency=50, order=3)
sim.get_model_manager().add_model(magnetic_model)

# Define the materials
air_material = TimeHarmonicMagneticGeneralMaterial.Constant("Air", "Air" @ Vol)

copper_material = TimeHarmonicMagneticGeneralMaterial.Constant("Copper", "Coil" @ Vol)

alu_material = TimeHarmonicMagneticGeneralMaterial.Constant(
    "Alu", "Plate" @ Vol, 1.0, 3.526e7
)

magnetic_model.add_materials([air_material, copper_material, alu_material])

# Coil
coil_model = ExcitationCoilModel()
sim.get_model_manager().add_model(coil_model)

coil_topology = CoilTopologyClosed(0.2, 0.01, 0.07, 1.0, 0.0, 0.0)
coil_type = CoilTypeStranded(2742)
coil_excitation = CoilExcitationCurrent.Constant(1.0)

coil = CoilSpecification(
    "Coil", "Coil" @ Vol, coil_topology, coil_type, coil_excitation
)
coil_model.add_coil_specification(coil)

# Run the code and output


sim.run()

vis = sim.get_field_exporter()

vis.add_field_output("MagneticFluxDensityReal")
vis.add_field_output("MagneticFluxDensityImag")
vis.add_field_output("MagneticFluxDensityAbs")

vis.save(order=3)

# Post Process Results


probe_reports = [("A1-B1", 0.072), ("A2-B2", 0.144)]
x_values = numpy.linspace(0.0, 0.288, 64)


for probe in probe_reports:

    b_values = []

    for x in x_values:

        magnetic_flux_density_real_report = mufem.ProbeReport.SinglePoint(
            name="MagneticFluxDensityRealReport",
            cff_name="MagneticFluxDensityReal",
            x=x,
            y=probe[1],
            z=0.034,
        )

        magnetic_flux_density_imag_report = mufem.ProbeReport.SinglePoint(
            name="MagneticFluxDensityImagReport",
            cff_name="MagneticFluxDensityImag",
            x=x,
            y=probe[1],
            z=0.034,
        )

        b_real = magnetic_flux_density_real_report.evaluate()
        b_imag = magnetic_flux_density_imag_report.evaluate()

        # We multiply by 1e3 to convert from T to mT
        # and by 1e3 to convert from m to mm
        b_values.append((1e3 * x, 1e3 * (-b_real.z + 1j * b_imag.z)))

    # Plot

    plt.clf()

    ref = numpy.loadtxt(
        f"{dir_path}/data/Bz_{probe[0]}.csv", delimiter=",", comments="#"
    )

    plt.plot(
        ref[:, 1],
        1.0e-1 * ref[:, 2],
        "ko-",
        label="Reference",
        markersize=6.5,
    )

    plt.plot(
        [x_value for x_value, _ in b_values],
        [numpy.real(b_value) for _, b_value in b_values],
        label=f"real",
        color="r",
    )

    plt.plot(
        ref[:, 1],
        1.0e-1 * ref[:, 3],
        "ko-",
    )

    plt.plot(
        [x_value for x_value, _ in b_values],
        [numpy.imag(b_value) for _, b_value in b_values],
        label=f"imag",
        color="b",
    )

    plt.xlabel("x [mm]")
    plt.ylabel("B [mT]")
    plt.title(f"Magnetic Flux Density at {probe[0]}")

    plt.savefig(
        f"{dir_path}/results/Magnetic_Flux_Density-{probe[0]}.png",
        bbox_inches="tight",
    )
