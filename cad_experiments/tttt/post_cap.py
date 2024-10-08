#!/usr/bin/env python3

from build123d import *
from jupyter_cadquery.viewer.client import show

cap_diameter = 49
cap_height = 48
tip_height = 8
tip_top_diameter = cap_diameter - 20 * 2


def build_part():
    with BuildPart() as part:
        cylinder_height = cap_height - tip_height
        cylinder = Cylinder(cap_diameter / 2, cylinder_height)

        with BuildSketch(Plane.XZ) as tip_profile:
            with BuildLine():
                bottom_y = cylinder_height / 2
                top_y = bottom_y + tip_height
                l1 = Line((0, top_y), (tip_top_diameter / 2, top_y))
                l2 = EllipticalCenterArc((tip_top_diameter / 2, bottom_y), 20, 8)
                l3 = Line(l2 @ 0, (0, bottom_y))
                l4 = Line(l3 @ 1, l1 @ 0)
            make_face()
        revolve(axis=Axis.Z)

        with BuildLine(Plane.XZ) as handle_path:
            minus_degrees = 18
            l1 = CenterArc((-15, 0, 0), 17, 90 + minus_degrees, 180 - minus_degrees * 2)
        with BuildSketch(Plane(origin=l1 @ 0, z_dir=l1 % 0)) as handle_profile:
            Ellipse(4 / 2, 10 / 2)
        handle = sweep()
        fillet(part.edges(Select.LAST), radius=1)

        with BuildSketch(Plane.XZ) as inside:
            with Locations((0, -cylinder_height / 2)):
                Trapezoid(42, 37, 90 - 4, align=(Align.CENTER, Align.MIN))
            fillet(inside.vertices().group_by(Axis.Y)[1], radius=3)
            split(bisect_by=Plane.YZ)
        revolve(axis=Axis.Z, mode=Mode.SUBTRACT)

    return part.part


part = build_part()

# Run script to update part in jupyter-cadquery
show(part)

# Reference implementation:
# I honestly think i like my implementation better!
# Although I did get the mass wrong the first time i checked it this time,
# because I didn't realize i needed to divide the handle profile dimensions
# by two when specifying the ellipse radii.

# with BuildPart() as p:
#     with BuildSketch(Plane.XZ) as sk1:
#         Rectangle(49, 48 - 8, align=(Align.CENTER, Align.MIN))
#         Rectangle(9, 48, align=(Align.CENTER, Align.MIN))
#         with Locations((9 / 2, 40)):
#             Ellipse(20, 8)
#         split(bisect_by=Plane.YZ)
#     revolve(axis=Axis.Z)

#     with BuildSketch(Plane.YZ.offset(-15)) as xc1:
#         with Locations((0, 40 / 2 - 17)):
#             Ellipse(10 / 2, 4 / 2)
#         with BuildLine(Plane.XZ) as l1:
#             CenterArc((-15, 40 / 2), 17, 90, 180)
#     sweep(path=l1)

#     fillet(p.edges().filter_by(GeomType.CIRCLE, reverse=True).group_by(Axis.X)[0], 1)

#     with BuildLine(mode=Mode.PRIVATE) as lc1:
#         PolarLine(
#             (42 / 2, 0), 37, 94, length_mode=LengthMode.VERTICAL
#         )  # construction line

#     pts = [
#         (0, 0),
#         (42 / 2, 0),
#         ((lc1.line @ 1).X, (lc1.line @ 1).Y),
#         (0, (lc1.line @ 1).Y),
#     ]
#     with BuildSketch(Plane.XZ) as sk2:
#         Polygon(*pts, align=None)
#         fillet(sk2.vertices().group_by(Axis.X)[1], 3)
#     revolve(axis=Axis.Z, mode=Mode.SUBTRACT)
