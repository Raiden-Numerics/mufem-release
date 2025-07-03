import numpy as np

from mufem import (
    Bnd,
    Vol,
    Everywhere,
    Simulation,
    SteadyRunner,
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


# Mesh ---------------------------------------------------------------------------------
xshifts = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]

mesh_files = [f"geometry_xshift={x:.1f}.msh" for x in xshifts]

sim.get_domain().load_mesh(mesh_files[0])
sim.get_domain().get_mesh().scale(1e-6)

refinement_model = RefinementModel()
sim.get_model_manager().add_model(refinement_model)


# Model --------------------------------------------------------------------------------
order = 1  # finite element polynomial degree
model = ElectrostaticsModel(Everywhere @ Vol, order)
sim.get_model_manager().add_model(model)

mesh_refiner = model.get_mesh_refiner()
mesh_refiner.set_refinement_fraction(0.6)


# Materials ----------------------------------------------------------------------------
eps = 1.0  # relative permittivity
material = ElectrostaticMaterial.Constant("Air", Everywhere @ Vol, eps)
model.add_material(material)


# Boundary conditions ------------------------------------------------------------------
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


# Reports ------------------------------------------------------------------------------
report = VolumeIntegralReport(
    name="Electric Energy Density Report", cff_name="Electric Energy Density",
)
sim.get_report_manager().add_report(report)


# Run the simulation -------------------------------------------------------------------
max_iterations = 25  # maximum number of iterations for each mesh file

max_ncells = 1e5  # maximum number of cells

vis = sim.get_field_exporter()
vis.add_field_output("Electric Potential")

for mesh_file in mesh_files:
    sim.get_domain().load_mesh(mesh_file)
    sim.get_domain().get_mesh().scale(1e-6)

    ncells = np.array([])
    energies = np.array([])

    for i in range(max_iterations):
        runner.advance(2)

        if i == 0:
            vis.save()

        nc = sim.get_domain().get_mesh().get_total_number_cells()

        ncells = np.append(ncells, nc)
        energies = np.append(energies, report.evaluate())

        if nc >= max_ncells:
            break
        else:
            refinement_model.refine_mesh()

    else:
        raise RuntimeError(
            "Maximum number of iterations reached without reaching max_ncells."
        )

    vis.save()


    # Save the results -----------------------------------------------------------------
    capacitances = 2 * energies / voltage**2  # [F]

    suffix = mesh_file.split('_')[-1][:-4]

    fname = f"results/Capacitance_{suffix}.csv"
    data = np.column_stack([ncells, capacitances])
    np.savetxt(fname, data, delimiter=", ", header="Number of cells, Capacitance [F]")
