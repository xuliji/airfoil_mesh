import pygmsh
import meshio
import numpy as np
import gmsh

resolution = 0.01


data = np.loadtxt("./picked_uiuc/2032c.dat")

geometry = pygmsh.geo.Geometry()
model = geometry.__enter__()
circle = model.add_polygon(data, holes=None, mesh_size=resolution)
points = [model.add_point((-0.5, -1, 0), mesh_size=resolution),
          model.add_point((1.5, -1, 0), mesh_size=resolution),
          model.add_point((1.5, 1, 0), mesh_size=resolution),
          model.add_point((-0.5, 1, 0), mesh_size=resolution)]

channel_lines = [model.add_line(points[i], points[i+1])
                 for i in range(-1, len(points)-1)]

channel_loop = model.add_curve_loop(channel_lines)
plane_surface = model.add_plane_surface(
    channel_loop, holes=[circle.curve_loop])
model.synchronize()
volume_marker = 6
model.add_physical([plane_surface], "Volume")
model.add_physical([channel_lines[0]], "Inflow")
model.add_physical([channel_lines[2]], "Outflow")
model.add_physical([channel_lines[1], channel_lines[3]], "Walls")
model.add_physical(circle.curve_loop.curves, "Obstacle")

geometry.generate_mesh(dim=2)
gmsh.write("mesh.msh")
gmsh.clear()
geometry.__exit__()