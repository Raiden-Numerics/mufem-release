import gmsh

gmsh.initialize()

# Setup the geometry -------------------------------------------------------------------
R = 10.0  # [m] sphere radius

tag_domain = gmsh.model.occ.add_sphere(xc=0, yc=0, zc=0, radius=R)

gmsh.model.occ.synchronize()

# Assign the name attributes -----------------------------------------------------------
# Define the tag of the outer boundary:
boundary = gmsh.model.get_boundary(dimTags=[(3, tag_domain)])
tag_outer = boundary[0][1]

gmsh.model.add_physical_group(dim=3, tags=[tag_domain], name="Domain", tag=1)
gmsh.model.add_physical_group(dim=2, tags=[tag_outer], name="Domain::Boundary", tag=1)

# Generate the mesh --------------------------------------------------------------------
gmsh.option.set_number(name="Mesh.MeshSizeMax", value=0.5)

gmsh.model.mesh.generate(dim=3)

# Write the mesh into file:
gmsh.option.set_number(name="Mesh.MshFileVersion", value=2.2)
gmsh.write(fileName="geometry.msh")

gmsh.finalize()