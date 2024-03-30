from svgpathtools import parse_path

def generate_shirt_sleeve_svg(sleeve_width_front=10, sleeve_height_front=30,
                              sleeve_width_back=10, sleeve_height_back=30,
                              sleeve_length=40, sleeve_width=45,
                              right_sleeve=True,
                              filename="tshirt_front.svg"):
    width = sleeve_height_front + sleeve_height_back
    shoulder = (sleeve_width_front + sleeve_width_back)/2
    point_a_x = 100
    point_a_y = 100
    point_b_x = point_a_x - ((width-sleeve_width)/2)
    point_b_y = point_a_y - (sleeve_length-shoulder)
    point_bbc_x = point_b_x + sleeve_width_front
    point_bbc_y = point_b_y
    point_bcc_x = point_b_x + (sleeve_height_front*0.25)
    point_bcc_y = point_b_y - sleeve_width_front
    point_c_x = point_b_x + sleeve_height_front
    point_c_y = point_b_y - sleeve_width_front
    point_ccd_x = point_c_x + (sleeve_height_back*0.75)
    point_ccd_y = point_c_y
    point_cdd_x = point_c_x + sleeve_height_back - sleeve_width_back
    point_cdd_y = point_c_y + sleeve_width_back
    point_d_x = point_c_x + sleeve_height_back
    point_d_y = point_c_y + sleeve_width_back
    point_e_x = point_d_x - ((width-sleeve_width)/2)
    point_e_y = point_d_y + (sleeve_length-shoulder)
    # Combine all the lines into one path
    path_d = " ".join([
        "M", str(point_a_x), str(point_a_y),  # Start (A)
        # where to start
        "L", str(point_b_x), str(point_b_y),
        "C", str(point_bbc_x), str(point_bbc_y), str(point_bcc_x), str(point_bcc_y), str(point_c_x), str(point_c_y),
        "C", str(point_ccd_x), str(point_ccd_y), str(point_cdd_x), str(point_cdd_y), str(point_d_x), str(point_d_y),
        "L", str(point_e_x), str(point_e_y),
        "L", str(point_a_x), str(point_a_y)
    ])

    path = parse_path(" ".join(
        ["M", str(point_b_x), str(point_b_y),
        "C", str(point_bbc_x), str(point_bbc_y), str(point_bcc_x), str(point_bcc_y), str(point_c_x), str(point_c_y),
        "C", str(point_ccd_x), str(point_ccd_y), str(point_cdd_x), str(point_cdd_y), str(point_d_x), str(point_d_y)]))
    print(path.length())

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
generate_shirt_sleeve_svg(filename="sleeve.svg")  # Generate SVG with curved neckline