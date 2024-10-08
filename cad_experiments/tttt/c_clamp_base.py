#!/usr/bin/env python3

from build123d import *
from jupyter_cadquery.viewer.client import show

width = 16
length = 95
height = 34


def build_clamp_base():
    with BuildPart() as part:
        with Locations((7, 0, 0)):
            Box(14, width, height)
        with Locations((0, 0, -1)):
            Box(length, width, 16, align=(Align.MIN, Align.CENTER, Align.MAX))
        with Locations((length - 9, 0, 0)):
            Box(18, width, height)

        fillet(part.edges().filter_by(Axis.Y).group_by(Axis.Z)[0], radius=18)
        fillet(part.edges().filter_by(Axis.Y).group_by(Axis.Z)[1], radius=7)

        with Locations((2.5, 0, 34 / 2)):
            start_cap = Cylinder(radius=16 / 2, height=23, rotation=(0, 90, 0))
        with Locations((length - 18 / 2, 0, 34 / 2)):
            Cylinder(radius=16 / 2, height=18, rotation=(0, 90, 0))

        with Locations(start_cap.faces().filter_by(Plane.YZ)[1]):
            CounterSinkHole(5.5 / 2, 11.2 / 2, counter_sink_angle=90)

    return part.part


# Run script to update part in jupyter-cadquery
part = build_clamp_base()
show(part)

# Reference implementation:
#
# with BuildPart() as ppp0103:
#     with BuildSketch() as sk1:
#         RectangleRounded(34 * 2, 95, 18)
#         with Locations((0, -2)):
#             RectangleRounded((34 - 16) * 2, 95 - 18 - 14, 7, mode=Mode.SUBTRACT)
#         with Locations((-34 / 2, 0)):
#             Rectangle(34, 95, 0, mode=Mode.SUBTRACT)
#     extrude(amount=16)
#     with BuildSketch(Plane.XZ.offset(-95 / 2)) as cyl1:
#         with Locations((0, 16 / 2)):
#             Circle(16 / 2)
#     extrude(amount=18)
#     with BuildSketch(Plane.XZ.offset(95 / 2 - 14)) as cyl2:
#         with Locations((0, 16 / 2)):
#             Circle(16 / 2)
#     extrude(amount=23)
#     with Locations(Plane.XZ.offset(95 / 2 + 9)):
#         with Locations((0, 16 / 2)):
#             CounterSinkHole(5.5 / 2, 11.2 / 2, None, 90)
