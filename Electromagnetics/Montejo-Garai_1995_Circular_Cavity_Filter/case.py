import matplotlib.pyplot as plt
import numpy

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
    name="Montejo-Garai_1995_Circular_Cavity_Filter", mesh_path="geometry.msh"
)

steady_runner = SteadyRunner(total_iterations=0)

# **************************************************************************************
# Markers
# **************************************************************************************
marker_input_port = "InputPort" @ Bnd
marker_output_port = "OutputPort" @ Bnd
marker_walls = "Walls" @ Bnd
marker_domain = "Domain" @ Vol

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
material_air = TimeHarmonicMaxwellGeneralMaterial.Vacuum("Air", marker_domain)
model.add_material(material_air)

# **************************************************************************************
# Boundary conditions
# **************************************************************************************
condition_pec = PerfectElectricConductorCondition("PEC", marker_walls)

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
Nf = 251  # number of frequencies to scan
frequencies = numpy.linspace(10e9, 15e9, Nf)  # [Hz] frequencies to scan

frequencies_paraview = [12e9, 14e9]  # [Hz] frequencies at which to save the field

vis = sim.get_visualization_helper()
vis.add_field_output("ElectricFieldReal")

S21 = numpy.zeros(Nf, dtype=complex)

for i, frequency in enumerate(frequencies):
    model.set_frequency(frequency)
    steady_runner.advance(1)

    if frequency in frequencies_paraview:
        vis.save()

    report_data = report_s_parameters.evaluate().to_numpy()
    S21[i] = report_data[0, 0]

# **************************************************************************************
# Plot the results
# **************************************************************************************
plt.clf()

# Reference data:
data = numpy.loadtxt("data/Montejo-Garai_1995.csv", delimiter=",")
f_GHz = data[:, 0]
S21_dB = data[:, 1]
plt.plot(f_GHz, S21_dB, "k^", label="Montejo-Garai 1995", markersize=10)

# Simulated data:
f_GHz = frequencies / 1e9
S21_abs2 = numpy.abs(S21) ** 2
S21_dB = 10 * numpy.log10(S21_abs2)
plt.plot(f_GHz, S21_dB, label="$\\mu$fem", color="red")

plt.legend(loc="best", frameon=False)
plt.xlabel("Frequency [GHz]")
plt.ylabel("|S21|$^2$ [dB]")
plt.savefig("results/S21_vs_frequency.png", bbox_inches="tight")
