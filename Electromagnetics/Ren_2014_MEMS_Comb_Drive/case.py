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


sim = Simulation.New(name="Ren_2014_MEMS_Comb_Drive")

runner = SteadyRunner(total_iterations=2)
sim.set_runner(runner)


# Mesh -----------------------------------------------------------------------------
nonconforming_options = NonConformingOption(
    is_nonconforming=True, simplicies_nonconforming=True
)

mesh_file = "geometry_xshift=0.0.msh"
sim.get_domain().load_mesh(mesh_file, nonconforming=nonconforming_options)
sim.get_domain().get_mesh().scale(1e-6)

refinement_model = RefinementModel()
sim.get_model_manager().add_model(refinement_model)


# Model ----------------------------------------------------------------------------
order = 1  # finite element polynomial degree
model = ElectrostaticsModel(Everywhere @ Vol, order)
sim.get_model_manager().add_model(model)

mesh_refiner = model.get_mesh_refiner()
mesh_refiner.set_refinement_fraction(0.6)


# Materials ------------------------------------------------------------------------
eps = 1.0  # relative permittivity
material = ElectrostaticMaterial.Constant("Air", Everywhere @ Vol, eps)
model.add_material(material)


# Boundary conditions --------------------------------------------------------------
voltage = 1  # [V]

condition_comb1 = ElectricPotentialCondition.Constant(
    "Comb1", "Comb1" @ Bnd, 0.0,
)

condition_comb2 = ElectricPotentialCondition.Constant(
    "Comb2", "Comb2" @ Bnd, voltage,
)

condition_ground = ElectricPotentialCondition.Constant(
    "Ground", "Ground" @ Bnd, 0.0,
)

model.add_conditions([condition_comb1, condition_comb2, condition_ground])


# Reports --------------------------------------------------------------------------
report = VolumeIntegralReport(
    name="Electric Energy Density Report", cff_name="Electric Energy Density",
)
sim.get_report_manager().add_report(report)


# Run the simulation ---------------------------------------------------------------
max_dofs = 15000  # maximum number of degrees of freedom

mesh_files = [
    "geometry_xshift=0.0.msh",
    "geometry_xshift=0.5.msh",
]

for mesh_file in mesh_files:
    sim.get_domain().load_mesh(mesh_file, nonconforming=nonconforming_options)
    sim.get_domain().get_mesh().scale(1e-6)


    dofs = np.array([])
    energies = np.array([])

    vis = sim.get_visualization_helper()
    vis.add_field_output("Electric Potential")

    initial_mesh = True

    while True:
        runner.advance(2)

        dofs = np.append(dofs, model.number_of_dofs())
        energies = np.append(energies, report.evaluate())

        if initial_mesh:
            vis.save()
            initial_mesh = False

        if model.number_of_dofs() >= max_dofs:
            break
        else:
            refinement_model.refine_mesh()

    vis.save()


    # Save the results -----------------------------------------------------------------
    capacitances = 2 * energies / voltage**2  # [F]

    suffix = mesh_file.split('_')[-1][:-4]

    fname = f"results/Capacitance_{suffix}.csv"
    data = np.column_stack([dofs, capacitances])
    np.savetxt(fname, data, delimiter=", ", header="Dofs, Capacitance [fF]")
