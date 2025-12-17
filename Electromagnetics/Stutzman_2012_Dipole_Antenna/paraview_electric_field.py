import paraview.simple as pvs


field_name = "Electric Field-Real"
field_unit = "V/m"
field_index = 0


# Load data ----------------------------------------------------------------------------
data = pvs.OpenDataFile(f"VisualizationOutput/Output_{field_index}.vtpc")


# Slice plane at z=0 -------------------------------------------------------------------
data = pvs.Slice(Input=data)
data.SliceType = "Plane"
data.SliceType.Origin = (0, 0, 0)
data.SliceType.Normal = (1, 0, 0)


# Translate ----------------------------------------------------------------------------
data = pvs.Transform(Input=data)
data.Transform.Translate = (0, 0, 1)


# View settings ------------------------------------------------------------------------
view = pvs.GetRenderView()

view.UseColorPaletteForBackground = 0
view.BackgroundColorMode = "Single Color"
view.Background = (1.0, 1.0, 1.0)
view.ViewSize = (1000, 1000)
view.OrientationAxesVisibility = 1
view.OrientationAxesLabelColor = (0.0, 0.0, 0.0)


# Display settings ---------------------------------------------------------------------
display = pvs.Show()


# Scalar bar settings ------------------------------------------------------------------
pvs.ColorBy(display, ("POINTS", field_name))

ctf = pvs.GetColorTransferFunction(field_name)
ctf.ApplyPreset("Cool to Warm")

scalar_bar = pvs.GetScalarBar(ctf)

scalar_bar.Title = f"{field_name} [V/m]"
scalar_bar.ComponentTitle = ""

scalar_bar.Orientation = "Horizontal"
scalar_bar.WindowLocation = "Lower Center"
scalar_bar.TitleColor = (0, 0, 0)
scalar_bar.LabelColor = (0, 0, 0)
scalar_bar.TitleFontSize = 32
scalar_bar.LabelFontSize = 28
scalar_bar.ScalarBarThickness = 32
scalar_bar.RangeLabelFormat = "%.0f"
scalar_bar.LabelFormat = "%.0f"

scalar_bar.LookupTable.RescaleTransferFunction(0, 30)


# Camera settings ----------------------------------------------------------------------
pvs.Render()

view.CameraViewUp = (0, 0, 1)
view.CameraPosition = (1, 0, 0)
view.CameraFocalPoint = (0, 0, 0)
view.CameraParallelProjection = 1
view.CameraParallelScale = 8


# Save screenshot ----------------------------------------------------------------------
pvs.SaveScreenshot("results/Scene_Electric_Field-Real.png")


pvs.Interact()
