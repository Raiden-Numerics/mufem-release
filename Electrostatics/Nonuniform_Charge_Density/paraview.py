import paraview.simple as pvs

# Input parameters:
data_file = "VisualizationOutput/Output_0.vtpc"
screenshot_file = "results/Scene_Electric_Field.png"

field_name = "Electric Field"
field_unit = "GV/m"

# Load data:
data = pvs.OpenDataFile(data_file)

# Slice settings:
data = pvs.Slice(Input=data)
data.SliceType = "Plane"
data.SliceType.Origin = [0, 0, 0]
data.SliceType.Normal = [0, 0, 1]

# Transform settings:
data = pvs.Transform(Input=data)
data.Transform.Translate = [0, 1, 0]

# Calculator settings:
data = pvs.Calculator(Input=data)
data.Function = '"Electric Field" / 1e9'
data.ResultArrayName = field_name

# View settings:
view = pvs.GetRenderView()
view.UseColorPaletteForBackground = 0
view.BackgroundColorMode = "Single Color"
view.Background = [1.0, 1.0, 1.0]
view.ViewSize = [900, 1000]
view.OrientationAxesVisibility = 1
view.OrientationAxesLabelColor = [0, 0, 0]

pvs.Render()

# Camera settings:
view.CameraViewUp = [0, 1, 0]
view.CameraPosition = [0, 0, 45]

# Display settings:
display = pvs.Show()
display.NonlinearSubdivisionLevel = 2

pvs.ColorBy(display, ("POINTS", field_name, "0"))

ctf = pvs.GetColorTransferFunction(field_name)
ctf.ApplyPreset("Cool to Warm")

# Scalar bar settings:
scalar_bar = pvs.GetScalarBar(ctf)
scalar_bar.Orientation = "Horizontal"
scalar_bar.WindowLocation = "Lower Center"
scalar_bar.TitleColor = [0, 0, 0]
scalar_bar.LabelColor = [0, 0, 0]
scalar_bar.ComponentTitle = ""
scalar_bar.Title = f"{field_name} [{field_unit}]"
scalar_bar.RangeLabelFormat = "%.0f"
scalar_bar.LabelFormat = "%.0f"
scalar_bar.LookupTable.RescaleTransferFunction([-1, 1])

pvs.Render()

pvs.SaveScreenshot(screenshot_file)

pvs.Delete(view)
pvs.Delete(data)
pvs.Delete(display)
