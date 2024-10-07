from math import radians, tan
from build123d import *
from jupyter_cadquery.viewer.client import show

from cad_experiments.utils import get_mass_g

length = 115
width = 50
outer_radius = 6

# First attempt: I couldn't figure out how to fillet the outer edge without
# also filleting the rest of the curved profile, since it all becomes a single
# edge once combined.
#
# with BuildPart() as part:
#     with BuildSketch(Plane.XZ.shift_origin((5.5, 0, 15)).offset(13)):
#         with BuildLine():
#             p1 = (0, 0)
#             p2 = (0, 27)
#             p3 = (26 * 2, 27)
#             p4 = (26 * 2, 0)
#             Line(p1, p2)
#             RadiusArc(p2, p3, 26)
#             Line(p3, p4)
#             Line(p4, p1)
#         make_face()

#     bearing_mount = extrude(amount=12)
#     with Locations(bearing_mount.faces().filter_by(Plane.XZ)[1]):
#         with Locations((0, -1, 0)):
#             CounterBoreHole(12, 17, 4)

#     mirror(about=Plane.XZ)

#     with BuildSketch():
#         RectangleRounded(length, 50, outer_radius)

#         # TODO: should be off-center
#         SlotOverall(90, 12, mode=Mode.SUBTRACT)

#     base = extrude(amount=15)

#     with BuildSketch(base.faces().filter_by(Plane.ZY)[0]):
#         # tan(ϑ) = o / a
#         # a * tan(ϑ) = o
#         # a = o / tan(ϑ)
#         bottom_width = 18
#         angle = 60
#         height = 8
#         top_width = bottom_width + height / tan(radians(angle))
#         Trapezoid(top_width, height, angle, align=(Align.CENTER, Align.MIN))

#     extrude(amount=-length, mode=Mode.SUBTRACT)

#     edge_set = part.faces().filter_by(Plane.XY)[0].edges().filter_by(Axis.Y)
#     fillet([edge_set[1], edge_set[3]], radius=9)

# fillet(part.faces().filter_by(Plane.YZ)[0].edges().filter_by(Axis.Z), radius=2)

# Second attempt: Fillet the overall shape, then build the details subtractively

total_height = 100
flange_width = 12

with BuildPart() as part2:
    with BuildSketch():
        RectangleRounded(length, width, outer_radius)
        with Locations((2.5, 0)):
            SlotOverall(90, 12, mode=Mode.SUBTRACT)
    container = extrude(amount=total_height)

    with BuildSketch(container.faces().filter_by(Plane.YZ)[0]):
        # tan(ϑ) = o / a
        # a * tan(ϑ) = o
        # a = o / tan(ϑ)
        bottom_width = 18
        angle = 60
        height = 8
        top_width = bottom_width + 2 * height / tan(radians(angle))
        with Locations((0, total_height / 2)):
            Trapezoid(top_width, height, angle, align=(Align.CENTER, Align.MAX))

    extrude(amount=-length, mode=Mode.SUBTRACT)

    with BuildSketch(container.faces().filter_by(Plane.XY)[1]):
        Rectangle(length, width - flange_width * 2)

    extrude(amount=-total_height + 15, mode=Mode.SUBTRACT)

    front_side = container.faces().filter_by(Plane.XZ)[0]
    back_side = container.faces().filter_by(Plane.XZ)[-1]
    with Locations(front_side):
        with Locations((-length / 2 + 26, -total_height / 2 + 42)):
            hole = CounterBoreHole(12, 17, 4, depth=flange_width)

    mirror(hole, about=Plane.XZ, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ) as sketch:
        with BuildLine():
            left = -length / 2
            p1 = (left, 100)
            p2 = (left, 42)
            p3 = (left + 26 * 2, 42)
            p4 = (left + 26 * 2, 15)
            p5 = (left + length, 15)
            p6 = (left + length, 100)
            l1 = Line(p1, p2)
            RadiusArc(l1 @ 1, p3, 26)
            FilletPolyline((p3, p4, p5), radius=9)
            Line(p5, p6)
            Line(p6, p1)
        make_face()

    extrude(amount=-width / 2, both=True, mode=Mode.SUBTRACT)

print(f"part mass: {get_mass_g(part2.part, 7800)}")

# Reference implementation:
# They ran into the same issue as I did with filleting, but instead
# of giving up and building a complex profile, they used extrude
# with intersect to round the corners. Nice trick!

# with BuildPart() as p:
#     with BuildSketch() as s:
#         Rectangle(115, 50)
#         with Locations((5 / 2, 0)):
#             SlotOverall(90, 12, mode=Mode.SUBTRACT)
#     extrude(amount=15)

#     with BuildSketch(Plane.XZ.offset(50 / 2)) as s3:
#         with Locations((-115 / 2 + 26, 15)):
#             SlotOverall(42 + 2 * 26 + 12, 2 * 26, rotation=90)
#     zz = extrude(amount=-12)
#     split(bisect_by=Plane.XY)
#     edgs = p.part.edges().filter_by(Axis.Y).group_by(Axis.X)[-2]
#     fillet(edgs, 9)

#     with Locations(zz.faces().sort_by(Axis.Y)[0]):
#         with Locations((42 / 2 + 6, 0)):
#             CounterBoreHole(24 / 2, 34 / 2, 4)
#     mirror(about=Plane.XZ)

#     with BuildSketch() as s4:
#         RectangleRounded(115, 50, 6)
#     extrude(amount=80, mode=Mode.INTERSECT)
#     # fillet does not work right, mode intersect is safer

#     with BuildSketch(Plane.YZ) as s4:
#         with BuildLine() as bl:
#             l1 = Line((0, 0), (18 / 2, 0))
#             l2 = PolarLine(l1 @ 1, 8, 60, length_mode=LengthMode.VERTICAL)
#             l3 = Line(l2 @ 1, (0, 8))
#             mirror(about=Plane.YZ)
#         make_face()
#     extrude(amount=115 / 2, both=True, mode=Mode.SUBTRACT)
