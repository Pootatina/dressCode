def generate_tshirt_front_svg(neckline_curve=False, neckline_width=30, neckline_length=60, filename="tshirt_front.svg"):
    if neckline_curve:
        # Calculate control point for neckline curve
        control_point_x = 915 - neckline_width / 2
        control_point_y = 60 + (neckline_length - 60)  # Ensure symmetry about the centerline

        # Define SVG content for the curved neckline
        neckline_svg = f'Q {control_point_x} {control_point_y} 915 60'
    else:
        # Calculate endpoint for straight neckline
        neckline_endpoint_x = 855 + neckline_width / 2
        neckline_endpoint_y = 60 + neckline_length

        # Define SVG content for the straight neckline
        neckline_svg = f'L 915 60 L {neckline_endpoint_x} {neckline_endpoint_y}'

    # Combine all the lines into one path
    path_d = " ".join([
        "M 738 387",  # Front Hem
        "L 738 387",  # Front Side Left
        "L 816 105",  # Front Sleeve Hole Left
        "Q 837.6 96.3 828 60",  # Shoulder Front Left
        f'{neckline_svg}',  # Neckline Front
        "L 942 60",  # Shoulder Front Right
        "Q 932.4 96.3 954 105",  # Front Sleeve Hole Right
        "L 1032 387",  # Front Side Right
        "L 738 387",  # Front Hem
    ])

    # Combine SVG content
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink" baseProfile="tiny" height="447px" version="1.2" width="1416px">
  <defs/>
  <path d="{path_d}" fill="none" stroke="black"/>
</svg>"""

    # Save SVG content to file
    with open(filename, "w") as f:
        f.write(svg_content)

    print(f"SVG pattern for front saved to {filename}")

# Example usage:
generate_tshirt_front_svg(neckline_curve=True, neckline_width=40, neckline_length=70, filename="curve.svg")  # Generate SVG with curved neckline
generate_tshirt_front_svg(neckline_curve=False, neckline_width=50, neckline_length=80, filename="edge.svg") # Generate SVG with straight neckline

