import paraview.simple as pvs

field_name = "Temperature"
field_unit = "K"

data = pvs.OpenDataFile("VisualizationOutput/Output_0.vtpc")

display = pvs.Show()

view = pvs.GetRenderView()
view.UseColorPaletteForBackground = 0
view.BackgroundColorMode = "Single Color"
view.Background = (1, 1, 1)
view.ViewSize = (1000, 1000)
view.OrientationAxesVisibility = 1
view.OrientationAxesLabelColor = (0, 0, 0)

pvs.Render()

view.CameraViewUp = (0, 1, 0)
view.CameraPosition = (0.3, 0.42, 2.2)
view.CameraFocalPoint = (0.3, 0.42, 0)

pvs.ColorBy(display, ("POINTS", field_name))

ctf = pvs.GetColorTransferFunction(field_name)
scalar_bar = pvs.GetScalarBar(ctf)
scalar_bar.Orientation = "Horizontal"
scalar_bar.WindowLocation = "Lower Center"
scalar_bar.TitleColor = (0, 0, 0)
scalar_bar.LabelColor = (0, 0, 0)
scalar_bar.TitleFontSize = 32
scalar_bar.LabelFontSize = 28
scalar_bar.ScalarBarThickness = 32
scalar_bar.ComponentTitle = ""
scalar_bar.Title = f"{field_name} [{field_unit}]"
scalar_bar.RangeLabelFormat = "%.0f"
scalar_bar.LabelFormat = "%.0f"
scalar_bar.LookupTable.RescaleTransferFunction(273, 373)

pvs.Render()

pvs.SaveScreenshot(f"results/Scene_{field_name}.png")

pvs.Delete(view)
pvs.Delete(data)
pvs.Delete(display)
