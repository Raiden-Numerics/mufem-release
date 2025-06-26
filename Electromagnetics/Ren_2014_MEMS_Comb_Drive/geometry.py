import gmsh


def create_geometry(xshift=0, mesh_file="geometry.msh", show=True):

    gmsh.initialize()


    # **********************************************************************************
    # Create geometry
    # **********************************************************************************
    u = 1  # unit of spatial dimensions


    def tooth(x, y, z):
        return gmsh.model.occ.addBox(x, y, z, 15 * u, 4 * u, 4 * u)

    # tag_ruler = gmsh.model.occ.addBox(0, 0, -2, 22*u, 4*u, 1*u)

    # Comb 1:
    tag_tooth1 = tooth(0, 0, 0)
    tag_tooth2 = tooth(0, 0, 10 * u)
    tag_tooth3 = tooth(0, 0, 20 * u)
    tag_tooth4 = tooth(0, 0, 30 * u)
    tag_base = gmsh.model.occ.addBox(0, 0, 0, 5 * u, 4 * u, 34 * u)

    ov = gmsh.model.occ.fuse(
        [(3, tag_base)],
        [(3, tag_tooth1), (3, tag_tooth2), (3, tag_tooth3), (3, tag_tooth4)],
    )
    comb1 = ov[0][0]

    gmsh.model.occ.translate([comb1], -xshift/2, 0, 0)

    # Comb 2:
    tag_tooth1 = tooth(7 * u, 0, 5 * u)
    tag_tooth1 = tooth(7 * u, 0, 5 * u + 10 * u)
    tag_tooth1 = tooth(7 * u, 0, 5 * u + 20 * u)
    tag_base = gmsh.model.occ.addBox(17 * u, 0, 0, 5 * u, 4 * u, 34 * u)

    ov = gmsh.model.occ.fuse(
        [(3, tag_base)], [(3, tag_tooth1), (3, tag_tooth2), (3, tag_tooth3)]
    )
    comb2 = ov[0][0]

    gmsh.model.occ.translate([comb2], +xshift/2, 0, 0)

    # Domain box:
    wx = 88 * u
    wy = 44 * u
    wz = 88 * u
    tag_domain = gmsh.model.occ.addBox(11 * u - wx / 2, -6 * u, 17 * u - wz / 2, wx, wy, wz)

    ov = gmsh.model.occ.cut([(3, tag_domain)], [comb1, comb2])
    domain = ov[0][0]


    gmsh.model.occ.synchronize()

    # **********************************************************************************
    # Assign attributes
    # **********************************************************************************
    print("3D: ", gmsh.model.getEntities(3))
    print("2D: ", gmsh.model.getEntities(2))

    comb1 = [(2, i) for i in range(1, 19)]
    comb2 = [(2, i) for i in range(19, 37)]
    ground = [(2, 38)]
    domain = [(3, 3)]

    gmsh.model.addPhysicalGroup(2, [dimTag[1] for dimTag in comb1], name="Comb1", tag=1)
    gmsh.model.addPhysicalGroup(2, [dimTag[1] for dimTag in comb2], name="Comb2", tag=2)
    gmsh.model.addPhysicalGroup(2, [dimTag[1] for dimTag in ground], name="Ground", tag=3)
    gmsh.model.addPhysicalGroup(3, [dimTag[1] for dimTag in domain], name="Domain", tag=1)


    # **********************************************************************************
    # Adjust the view
    # **********************************************************************************
    gmsh.model.setColor(domain, 153, 191, 242, recursive=True)
    gmsh.model.setColor(comb1, 240, 160, 81, recursive=True)
    gmsh.model.setColor(comb2, 170, 248, 198, recursive=True)
    gmsh.model.setColor(ground, 100, 100, 100, recursive=True)

    gmsh.option.setNumber("General.BackgroundGradient", 0)

    gmsh.option.setNumber("General.Trackball", 0)
    gmsh.option.setNumber("General.RotationX", 45)
    gmsh.option.setNumber("General.RotationY", -50)

    scale = 0.9
    gmsh.option.setNumber("General.ScaleX", scale)
    gmsh.option.setNumber("General.ScaleY", scale)
    gmsh.option.setNumber("General.ScaleZ", scale)

    gmsh.option.setNumber("Mesh.SurfaceEdges", 1)
    gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
    gmsh.option.setNumber("Mesh.VolumeEdges", 0)
    gmsh.option.setNumber("Mesh.VolumeFaces", 0)

    gmsh.option.setNumber("General.Clip0A", 0)
    gmsh.option.setNumber("General.Clip0B", -1)
    gmsh.option.setNumber("General.Clip0D", 4.01 * u)
    gmsh.option.setNumber("Mesh.Clip", 1)


    # **********************************************************************************
    # Generate mesh
    # **********************************************************************************
    maxh = 4 * u
    gmsh.option.setNumber("Mesh.MeshSizeMax", maxh)

    gmsh.model.mesh.generate(3)

    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
    gmsh.write(mesh_file)

    # Save to image file:
    # gmsh.fltk.initialize()
    # gmsh.graphics.draw()
    # gmsh.option.setNumber("Print.Width", 800)
    # gmsh.option.setNumber("Print.Height", 1200)
    # gmsh.write("Geometry.png")
    # gmsh.fltk.finalize()

    if show:
        gmsh.fltk.run()

    gmsh.finalize()


if __name__ == "__main__":

    for xshift in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]:

        mesh_file = f"geometry_xshift={xshift:.1f}.msh"

        create_geometry(xshift=xshift, mesh_file=mesh_file, show=False)
