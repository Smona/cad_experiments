#!/usr/bin/env python3
from build123d import Box
from yacv_server import show_all

length, width, thickness = 10.0, 60.0, 10.0

ex1 = Box(length, width, thickness)
ex2 = Box(length, width, thickness, rotation=(0, 20, 90))

show_all()
