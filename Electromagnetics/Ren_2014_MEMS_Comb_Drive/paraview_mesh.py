import sys
sys.path.insert(0, '/home/fedoroff/software/ParaView-5.13.20250312-MPI-Linux-Python3.12-x86_64/lib/python3.12/site-packages/')

import paraview.simple as pvs


def create_scene(data_file, screenshot_file, show=False):
    field_name = "Electric Potential"
    field_unit = "V"

    # View settings:
    view = pvs.GetRenderView()
    view.UseColorPaletteForBackground = 0
    view.BackgroundColorMode = "Single Color"
    view.Background = [1.0, 1.0, 1.0]
    view.ViewSize = [1100, 800]
    view.OrientationAxesVisibility = 1
    view.OrientationAxesLabelColor = [1, 1, 1]

    pvs.Render()

    # Camera settings:
    view.CameraViewUp = [-1, 0, 0]
    view.CameraPosition = [0, 1e-4, 0]
    view.CameraFocalPoint = [0.0, 0.0, 0.0]
    view.CameraFocalDisk = 1.0
    view.CameraParallelProjection = 1
    view.CameraParallelScale = 2e-5
    view.CenterOfRotation = [0.0, 0.0, 0.0]

    data = pvs.OpenDataFile(data_file)

    # Slice settings:
    data = pvs.Slice(Input=data)
    data.SliceType = "Plane"
    data.SliceType.Origin = [11e-6, 2e-6, 17e-6]
    data.SliceType.Normal = [0, 1, 0]

    # Transform settings:
    data = pvs.Transform(Input=data)
    data.Transform.Translate = [-15e-6, 0, -17e-6]

    # Display settings:
    display = pvs.Show()
    display.Representation = "Surface With Edges"
    display.EdgeColor = [0.1, 0.1, 0.1]
    display.LineWidth = 1
    display.NonlinearSubdivisionLevel = 1

    pvs.ColorBy(display, ("POINTS", field_name))

    ctf = pvs.GetColorTransferFunction(field_name)
    ctf.ApplyPreset("Cool to Warm")

    # Scalar bar settings:
    scalar_bar = pvs.GetScalarBar(ctf)
    scalar_bar.Orientation = "Horizontal"
    scalar_bar.WindowLocation = "Lower Center"
    scalar_bar.TitleColor = [1, 1, 1]
    scalar_bar.LabelColor = [1, 1, 1]
    scalar_bar.TitleFontSize = 28
    scalar_bar.LabelFontSize = 20
    scalar_bar.ScalarBarThickness = 28
    scalar_bar.ComponentTitle = ""
    scalar_bar.Title = f"{field_name} [{field_unit}]" if field_unit else field_name
    scalar_bar.RangeLabelFormat = "%.0f"
    scalar_bar.LabelFormat = "%.0f"
    scalar_bar.LookupTable.RescaleTransferFunction([0, 1])

    pvs.Render()

    pvs.SaveScreenshot(screenshot_file)

    if show:
        pvs.Interact()

    pvs.Delete(view)
    pvs.Delete(data)
    pvs.Delete(display)



if __name__ == "__main__":
    data_file = "VisualizationOutput/Output_0.vtpc"
    screenshot_file = f"results/Scene_Electric_Potential_0_Mesh.png"
    create_scene(data_file, screenshot_file)

    data_file = "VisualizationOutput/Output_1.vtpc"
    screenshot_file = f"results/Scene_Electric_Potential_1_Mesh.png"
    create_scene(data_file, screenshot_file)