import paraview.simple as pvs


# **************************************************************************************
# Setup the view
# **************************************************************************************
view = pvs.GetRenderView()
view.ViewSize = [1200, 650]
view.OrientationAxesVisibility = 0

# Need to call the render in advance to keep the camera properties, since if this is the
# first render and the view is a RenderView, the camera is reset:
# https://www.paraview.org/paraview-docs/nightly/python/paraview.simple.html#paraview.simple.Render
pvs.Render()

wr75_length = 20e-3
iris_length = 1e-3
cavity_length = 100e-3
total_length = wr75_length + iris_length + cavity_length + iris_length + wr75_length

camera = view.GetActiveCamera()
camera.SetFocalPoint(0, 0, total_length / 2)
camera.SetPosition(-0.6830, 0.2588, -0.6830)
camera.SetParallelProjection(1)
camera.SetParallelScale(0.03)  # zoom


# **************************************************************************************
# Electric field at 12 GHz
# **************************************************************************************
data = pvs.OpenDataFile("VisualizationOutput/Output_0.vtpc")

blocks = pvs.ExtractBlock(Input=data)
blocks.Selectors = ["/Root/Domain"]
display = pvs.Show()

pvs.ColorBy(display, ("POINTS", "ElectricFieldReal", "Magnitude"))

ctf = pvs.GetColorTransferFunction("ElectricFieldReal")
ctf.ApplyPreset("Cool to Warm")
ctf.RescaleTransferFunction(0, 150)

scalar_bar = pvs.GetScalarBar(ctf)
scalar_bar.Orientation = "Horizontal"
scalar_bar.WindowLocation = "Lower Center"
scalar_bar.TitleColor = [0, 0, 0]
scalar_bar.LabelColor = [0, 0, 0]
scalar_bar.Title = "Electric Field [V/m]"
scalar_bar.ComponentTitle = ""
scalar_bar.UseCustomLabels = True
scalar_bar.CustomLabels = [0, 50, 100, 150]

pvs.Render()
pvs.SaveScreenshot(
    "results/scene_electric_field_12GHz.png",
    OverrideColorPalette="WhiteBackground",
)

# **************************************************************************************
# Electric field at 14 GHz
# **************************************************************************************
data = pvs.OpenDataFile("VisualizationOutput/Output_1.vtpc")

blocks = pvs.ExtractBlock(Input=data)
blocks.Selectors = ["/Root/Domain"]
display = pvs.Show()

pvs.ColorBy(display, ("POINTS", "ElectricFieldReal", "Magnitude"))

ctf = pvs.GetColorTransferFunction("ElectricFieldReal")
ctf.ApplyPreset("Cool to Warm")
ctf.RescaleTransferFunction(0, 150)

scalar_bar = pvs.GetScalarBar(ctf)
scalar_bar.Orientation = "Horizontal"
scalar_bar.WindowLocation = "Lower Center"
scalar_bar.TitleColor = [0, 0, 0]
scalar_bar.LabelColor = [0, 0, 0]
scalar_bar.Title = "Electric Field [V/m]"
scalar_bar.ComponentTitle = ""
scalar_bar.UseCustomLabels = True
scalar_bar.CustomLabels = [0, 50, 100, 150]

pvs.Render()
pvs.SaveScreenshot(
    "results/scene_electric_field_14GHz.png",
    OverrideColorPalette="WhiteBackground",
)
