import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

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


def main(mesh_file):
    sim = Simulation.New(name="Ren_2014_MEMS_Comb_Drive")

    runner = SteadyRunner(total_iterations=2)
    sim.set_runner(runner)


    # Mesh -----------------------------------------------------------------------------
    nonconforming_options = NonConformingOption(
        is_nonconforming=True, simplicies_nonconforming=True
    )

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

    # if sim.get_machine().is_main_process():
    #     dst = f"results/VisualizationOutput_{suffix}"
    #     if os.path.exists(dst):
    #         shutil.rmtree(dst)
    #     shutil.move("VisualizationOutput", dst)


if __name__ == "__main__":
    mesh_file = "geometry_xshift=0.0.msh"
    # mesh_file = "geometry_xshift=0.5.msh"
    # mesh_file = "geometry_xshift=1.0.msh"
    # mesh_file = "geometry_xshift=1.5.msh"
    # mesh_file = "geometry_xshift=2.0.msh"
    # mesh_file = "geometry_xshift=2.5.msh"
    # mesh_file = "geometry_xshift=3.0.msh"
    # mesh_file = "geometry_xshift=3.5.msh"
    # mesh_file = "geometry_xshift=4.0.msh"
    # mesh_file = "geometry_xshift=4.5.msh"
    # mesh_file = "geometry_xshift=5.0.msh"
    # mesh_file = "geometry_xshift=5.5.msh"
    # mesh_file = "geometry_xshift=6.0.msh"
    # mesh_file = "geometry_xshift=6.5.msh"
    # mesh_file = "geometry_xshift=7.0.msh"
    # mesh_file = "geometry_xshift=7.5.msh"
    # mesh_file = "geometry_xshift=8.0.msh"

    main(mesh_file)
