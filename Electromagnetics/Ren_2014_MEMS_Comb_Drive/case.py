import matplotlib.pyplot as plt
import numpy as np

from mufem import (
    Bnd,
    Vol,
    Everywhere,
    Simulation,
    SteadyRunner,
    NonConformingOption,
    RefinementModel,
    VolumeIntegralReport,
)
from mufem.electromagnetics.electrostatics import (
    ElectricPotentialCondition,
    ElectrostaticMaterial,
    ElectrostaticsModel,
)


# **************************************************************************************
# Problem setup
# **************************************************************************************
sim = Simulation.New(
    name="Ren_2014_MEMS_Comb_Drive"
)

# is_main_process = sim.get_machine().is_main_process()

steady_runner = SteadyRunner(total_iterations=2)
sim.set_runner(steady_runner)


# **************************************************************************************
# Mesh
# **************************************************************************************
nonconforming_options = NonConformingOption(
    is_nonconforming=True, simplicies_nonconforming=True
)

sim.get_domain().load_mesh(
   "geometry.msh", nonconforming=nonconforming_options
)
sim.get_domain().get_mesh().scale(1e-6)

refinement_model = RefinementModel()
sim.get_model_manager().add_model(refinement_model)


# **************************************************************************************
# Model
# **************************************************************************************
order = 1  # finite element polynomial degree
model = ElectrostaticsModel(Everywhere @ Vol, order)
sim.get_model_manager().add_model(model)

mesh_refiner = model.get_mesh_refiner()
mesh_refiner.set_refinement_fraction(0.6)


# **************************************************************************************
# Materials
# **************************************************************************************
eps = 1.0  # relative permittivity
material = ElectrostaticMaterial.Constant("Air", Everywhere @ Vol, eps)
model.add_material(material)


# **************************************************************************************
# Boundary conditions
# **************************************************************************************
condition_comb1 = ElectricPotentialCondition.Constant("Comb1", "Comb1" @ Bnd, 0.0)

condition_comb2 = ElectricPotentialCondition.Constant("Comb2", "Comb2" @ Bnd, 1.0)

condition_ground = ElectricPotentialCondition.Constant("Ground", "Ground" @ Bnd, 0.0)

model.add_conditions([condition_comb1, condition_comb2, condition_ground])


# **************************************************************************************
# Reports
# **************************************************************************************
report = VolumeIntegralReport(
    name="Electric Energy Density Report", cff_name="Electric Energy Density",
)
sim.get_report_manager().add_report(report)


# **************************************************************************************
# Run the simulation
# **************************************************************************************
# number of mesh refinement cycles + 1 (including the initial mesh):
nref_with_initial = 21

ne = np.zeros(nref_with_initial)
energy = np.zeros(nref_with_initial)

vis = sim.get_visualization_helper()
vis.add_field_output("Electric Potential")

for n in range(nref_with_initial):
    if n > 0:
        refinement_model.refine_mesh()

    steady_runner.advance(2)

    ne[n] = sim.get_domain().get_mesh().get_number_cells()
    print(ne[n])

    energy[n] = report.evaluate()

vis.save(order=2)


# **************************************************************************************
# Plot the results
# **************************************************************************************
voltage = 1  # [V]
capacitance = 2 * energy / voltage**2  # [F]

plt.figure()
plt.plot(ne / 1e3, capacitance / 1e-15)
plt.xlabel("Number of elements (10³)")
plt.ylabel("Capacitance [fF]")
plt.savefig("results/Capacitance.png", bbox_inches="tight")


data = np.stack([ne/1e3, capacitance/1e-15])
np.savetxt("out.dat", data.T, header="Number of elements (10³), Capacitance [fF]", delimiter=", ")