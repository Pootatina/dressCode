def generate_tshirt_sleeve_svg(sleeve_width=40, sleeve_length=80, filename="tshirt_sleeve.svg"):
    # Calculate control point for sleeve curves
    control_point_x = 600 - sleeve_width / 2
    control_point_y = 60 + (sleeve_length - 60)  # Ensure symmetry about the centerline

    # Define SVG content for the curved sleeve
    sleeve_curves_svg = f'Q {control_point_x} {control_point_y} 600 60'

    # Combine all the lines into one path
    path_d = " ".join([
        "M 384 387",  # Sleeve Hem
        "L 384 387",  # Sleeve Side Left
        "L 516 120",  # Sleeve Hole Left
        f'{sleeve_curves_svg}',  # Sleeve Curves
        "L 684 120",  # Sleeve Hole Right
        "L 816 387",  # Sleeve Side Right
        "L 384 387",  # Sleeve Hem
    ])

    # Combine SVG content
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink" baseProfile="tiny" height="447px" version="1.2" width="1416px">
  <defs/>
  <path d="{path_d}" fill="none" stroke="black"/>
</svg>"""

    # Save SVG content to file
    with open(filename, "w") as f:
        f.write(svg_content)

    print(f"SVG pattern for sleeve saved to {filename}")

# Example usage:
generate_tshirt_sleeve_svg(sleeve_width=50, sleeve_length=90)  # Generate SVG for sleeve
