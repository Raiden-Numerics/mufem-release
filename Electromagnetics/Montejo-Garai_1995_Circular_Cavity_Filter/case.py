import numpy
import pylab

from mufem import Bnd, Vol, Simulation, SteadyRunner
from mufem.electromagnetics.timeharmonicmaxwell import (
    InputPortCondition,
    OutputPortCondition,
    PerfectElectricConductorCondition,
    SParametersReport,
    TimeHarmonicMaxwellGeneralMaterial,
    TimeHarmonicMaxwellModel,
)


# **************************************************************************************
# Problem setup
# **************************************************************************************
sim = Simulation.New(
    name="Montejo-Garai_1995_Circular_Cavity_Filter", mesh_path="geometry.mesh"
)

steady_runner = SteadyRunner(total_iterations=0)

# **************************************************************************************
# Markers
# **************************************************************************************
marker_domain = "Filter" @ Vol
marker_pec_walls = "Filter::PEC" @ Bnd
marker_input_port = "Filter::Input" @ Bnd
marker_output_port = "Filter::Output" @ Bnd

# **************************************************************************************
# Model
# **************************************************************************************
frequency = 14.5e9  # [Hz] radiation frequency
order = 2  # finite element polynomial degree
model = TimeHarmonicMaxwellModel(marker_domain, frequency, order)
sim.get_model_manager().add_model(model)

# **************************************************************************************
# Materials
# **************************************************************************************
air_material = TimeHarmonicMaxwellGeneralMaterial.Vacuum("Air", marker_domain)
model.add_material(air_material)

# **************************************************************************************
# Boundary conditions
# **************************************************************************************
condition_pec = PerfectElectricConductorCondition("PEC", marker_pec_walls)

mode_index = 0  # index of the mode that will be launched from the input port
condition_input_port = InputPortCondition("Input", marker_input_port, mode_index)

condition_output_port = OutputPortCondition("Output", marker_output_port)

model.add_conditions([condition_pec, condition_input_port, condition_output_port])

# **************************************************************************************
# Reports
# **************************************************************************************
nmodes = 1  # number of modes to be calculated for the report
report_s_parameters = SParametersReport("S-parameters", condition_output_port, nmodes)
sim.get_report_manager().add_report(report_s_parameters)

# **************************************************************************************
# Run the simulation
# **************************************************************************************
Nf = 100  # number of frequencies to scan
frequencies = numpy.linspace(10e9, 15e9, Nf)  # [Hz] frequencies to scan

S21 = numpy.zeros(Nf, dtype=complex)

for i, frequency in enumerate(frequencies):
    model.set_frequency(frequency)
    steady_runner.advance(1)

    report_data = report_s_parameters.evaluate().to_numpy()
    S21[i] = report_data[0, 0]

# **************************************************************************************
# Plot the results
# **************************************************************************************
pylab.clf()

# Reference data:
data = numpy.loadtxt("data/Montejo-Garai_1995.csv", delimiter=",")
f_GHz = data[:, 0]
S21_dB = data[:, 1]
pylab.plot(f_GHz, S21_dB, "k^", label="Montejo-Garai 1995", markersize=10)

# Simulated data:
f_GHz = frequencies / 1e9
S21_abs2 = numpy.abs(S21) ** 2
S21_dB = 10 * numpy.log10(S21_abs2)
pylab.plot(f_GHz, S21_dB, label="$\\mu$fem", color="red")

pylab.legend(loc="best", frameon=False)
pylab.xlabel("Frequency [GHz]")
pylab.ylabel("|S21|$^2$ [dB]")
pylab.savefig("results/transmission_spectrum.png", bbox_inches="tight")
