#!/usr/bin/env python3
from build123d import *
from jupyter_cadquery.viewer.client import show

with BuildPart() as part:
    s1 = Cylinder(38 / 2, 21 + 7 - 8)
    with Locations(s1.faces().filter_by(Plane.XY)[0]):
        s2 = Cylinder(26 / 2, 8 * 2)

    with Locations((0, 0, -6.5)):
        Cylinder(80, 7)
    fillet(part.edges().filter_by(Plane.XY)[0], radius=4)

    with Locations(s2.faces().filter_by(Plane.XY)[0]):
        Hole(16 / 2)

    with BuildSketch():
        SlotCenterPoint(center=(80, 0), point=(0, 0), height=38)
        split(bisect_by=Plane.YZ.offset(80 - 38 / 2), keep=Keep.BOTTOM)
    extrude(amount=20, both=True, mode=Mode.INTERSECT)

    with Locations((61 - 5, 0, -18)):
        dangler = Box(10, 38, 30)

    fillet(part.edges().filter_by(Axis.Y)[0], radius=5)
    fillet(part.edges().filter_by(Axis.Y)[4], radius=10)

    end_face = part.faces().filter_by(Plane.YZ)[0]
    bottom_edge = end_face.edges().filter_by(Axis.Y)[1]
    slot_origin = bottom_edge.center()
    slot_plane = Plane(origin=slot_origin, z_dir=end_face.normal_at())
    center_point = (17 - 9, 0)
    with BuildSketch(slot_plane):
        SlotCenterPoint(center=(0, 0), point=center_point, height=9 * 2)
    extrude(amount=-5, mode=Mode.SUBTRACT)

    with BuildSketch(slot_plane):
        SlotCenterPoint(center=(0, 0), point=center_point, height=6 * 2)
    extrude(amount=-10, mode=Mode.SUBTRACT)

part = part.part
show(part)
