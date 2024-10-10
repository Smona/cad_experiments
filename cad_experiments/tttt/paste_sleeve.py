#!/usr/bin/env python3

from build123d import *
from jupyter_cadquery.viewer.client import show

with BuildPart() as part:
    for thickness, mode in ((3, Mode.ADD), (0, Mode.SUBTRACT)):
        diff = thickness * 2
        with BuildSketch() as bottom_profile:
            SlotOverall(width=45 + diff, height=38 + diff)
        with BuildSketch(Plane.XY.offset(103)) as top_profile:
            SlotOverall(width=60 + diff, height=4 + diff)

        top = loft(mode=mode)
        extrude(top.faces().filter_by(Plane.XY)[0], amount=30, mode=mode)

show(part)