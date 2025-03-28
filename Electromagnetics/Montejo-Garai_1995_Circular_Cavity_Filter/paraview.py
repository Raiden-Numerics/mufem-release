import paraview.simple as pvs


# **************************************************************************************
# Setup the view
# **************************************************************************************
view = pvs.GetRenderView()
view.ViewSize = [1200, 1000]
view.CameraPosition = [-0.6830, 0.2588, -0.6830]
view.CameraParallelProjection = 1  # enable orthographic (parallel) projection
view.OrientationAxesVisibility = 0

# view.CameraViewAngle = 1
camera = view.GetActiveCamera()
camera.ViewAngle = 3

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

pvs.Render()
pvs.SaveScreenshot(
    "results/scene_electric_field_14GHz.png",
    OverrideColorPalette="WhiteBackground",
)
