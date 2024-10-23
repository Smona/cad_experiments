#!/usr/bin/env python3

import math
from build123d import *
from jupyter_cadquery.viewer.client import show

with BuildPart() as part:
    with Locations(Plane.XZ):
        cylinder = Cylinder(30 / 2, 36)

    with Locations(Plane.XZ.offset((22 - 36) / 2)):
        Cylinder(30 / 2 + 7, 22)

    fillet(part.edges().filter_by(Plane.XZ)[1], radius=6)

    with BuildSketch(
        cylinder.faces().filter_by(Plane.XZ)[1].rotate(Axis.Y, 180)
    ) as profile:
        top_slot_center = 69 - 30 / 2 - 10
        with Locations((0, top_slot_center)):
            SlotCenterToCenter(44, 10 * 2)
            split(bisect_by=Plane.YZ)
        y_offset = (44 / 2) / math.tan(math.radians(45))
        SlotCenterPoint(
            (0, top_slot_center - y_offset), (44 / 2, top_slot_center), 10 * 2
        )
        with Locations((44 / 2, top_slot_center)):
            Circle(13 / 2, mode=Mode.SUBTRACT)
        split(bisect_by=Plane.ZX.offset(22))

        SlotCenterPoint((0, 69 - 30 / 2), (0, 0), 30)
        split(bisect_by=Plane.XZ.offset(-69 + 30 / 2))
        fillet(profile.vertices().group_by(Axis.Y)[1], radius=12)

        mirror(about=Plane.YZ)
    extrude(profile.sketch, amount=-36, mode=Mode.INTERSECT)
    extrude(profile.sketch, amount=-22)

    with BuildSketch(part.faces().filter_by(Plane.XZ)[0]) as hole:
        Circle(12 / 2)
        Rectangle(4, 15 - 12 / 2, align=(Align.CENTER, Align.MIN))
    extrude(hole.sketch, amount=-36, mode=Mode.SUBTRACT)

    with BuildSketch(part.faces().filter_by(Plane.XY)[0]) as slot:
        Rectangle(44 + 10 * 2, 10)
    extrude(slot.sketch, amount=-42, mode=Mode.SUBTRACT)


show(part)
