from svgpathtools import parse_path


def generate_shirt_front_svg(side_width_front=5, side_height_front=40,
                             neckline_width_front=20, neckline_height_front=50,
                             sleeve_width_front=10, sleeve_height_front=30,
                             shoulder_width_front=15, shoulder_height_front=5,
                             width=80, length=60,
                             filename="tshirt_front.svg"):
    width_all = (2 * sleeve_width_front) + (2 * shoulder_width_front) + neckline_width_front
    point_a_x = 100
    point_a_y = 100
    point_b_x = point_a_x + side_width_front
    point_b_y = point_a_y - side_height_front
    point_bc_x = point_b_x + sleeve_width_front
    point_bc_y = point_b_y  # maybe minus something
    point_c_x = point_b_x + sleeve_width_front
    point_c_y = point_b_y - sleeve_height_front
    point_d_x = point_c_x + shoulder_width_front
    point_d_y = point_c_y - shoulder_height_front
    point_e_x = point_d_x + neckline_width_front
    point_e_y = point_d_y
    point_f_x = point_e_x + shoulder_width_front
    point_f_y = point_e_y + shoulder_height_front
    point_fg_x = point_f_x
    point_fg_y = point_f_y + sleeve_height_front
    point_g_x = point_f_x + sleeve_width_front
    point_g_y = point_f_y + sleeve_height_front
    point_h_x = point_g_x + side_width_front
    point_h_y = point_g_y + side_height_front
    # Combine all the lines into one path
    path_d = " ".join([
        "M", str(point_a_x), str(point_a_y),  # Start (A)
        # where to start
        "L", str(point_b_x), str(point_b_y),  # Front Side Left (B) 1000 1400
        # could be in winkel
        "Q", str(point_bc_x), str(point_bc_y), str(point_c_x), str(point_c_y),  # Front Sleeve Hole Left (C)
        "L", str(point_d_x), str(point_d_y),  # Shoulder Front Right (D)
        "A", str(neckline_width_front / 2)  # radius x achse ellipse
        , str(neckline_height_front)  # radius y achse ellipse
        , "0 0 0",
        str(point_e_x), str(point_e_y),
        "L", str(point_f_x), str(point_f_y),  # Shoulder right (F)
        "Q", str(point_fg_x), str(point_fg_y), str(point_g_x), str(point_g_y),  # Front Sleeve Hole right (G)
        "L", str(point_h_x), str(point_h_y),  # Front Side Right
        "L", str(point_a_x), str(point_a_y)  # Front Hem
    ])
    path = parse_path(" ".join(
        ["M", str(point_b_x), str(point_b_y), "Q", str(point_bc_x), str(point_bc_y), str(point_c_x), str(point_c_y)]))
    print(path.length()-2)
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
generate_shirt_front_svg(filename="front.svg")  # Generate SVG with curved neckline
