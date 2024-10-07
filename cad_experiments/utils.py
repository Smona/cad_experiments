#!/usr/bin/env python3
from build123d import LineType, Part, Compound, ExportSVG, Rectangle, export_stl
from IPython.display import publish_display_data


def export_image(part: Part, path: str):
    svg_path = f"renders/{path}.svg"
    stl_path = f"meshes/{path}.stl"
    view_port_origin = (-100, -50, 30)

    visible, hidden = part.project_to_viewport(view_port_origin)
    bbox = Compound(visible + hidden).bounding_box()
    max_dimension = max(*bbox.size)
    exporter = ExportSVG(
        scale=150 / max_dimension, fill_color=(30, 30, 46), line_color=None
    )
    exporter.add_layer("Visible", line_color=(200, 200, 200))
    exporter.add_layer("Hidden", line_color=(99, 99, 99), line_type=LineType.ISO_DOT)
    exporter.add_shape(Rectangle(width=bbox.size.X * 1.2, height=bbox.size.Y * 1.2))
    exporter.add_shape(visible, layer="Visible")
    exporter.add_shape(hidden, layer="Hidden")
    exporter.write(svg_path)

    export_stl(part, stl_path, ascii_format=True)

    message = f"""
    [[file:{svg_path}]]      [[file:{stl_path}][STL file]]
    """
    publish_display_data({"text/org": message})


def get_mass_g(part: Part, density_kg_m3: float) -> float:
    volume_m3 = part.volume / 1000**3
    mass_kg = volume_m3 * density_kg_m3
    return mass_kg * 1000
