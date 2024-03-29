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
        "M 10 10",  # Front Hem
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

def generate_tshirt_front_svg_cm(height_side=40, width_side=5, width_neckline=20 , width_shoulder=15, width_arm=10, height_arm=20, height_shoulder=5, neckline_deep=30, width=80, length=60, filename="tshirt_front.svg"):
    width_all=(2*width_arm)+(2*width_shoulder)+width_neckline
    point_a_x = 100
    point_a_y = 100
    point_b_x = point_a_x + width_side
    point_b_y = point_a_y - height_side
    point_bc_x = point_b_x + width_arm
    point_bc_y = point_b_y #maybe minus something
    point_c_x = point_b_x + width_arm
    point_c_y = point_b_y - height_arm
    point_d_x = point_c_x + width_shoulder
    point_d_y = point_c_y - height_shoulder
    point_e_x = point_d_x + width_neckline
    point_e_y = point_d_y
    point_f_x = point_e_x + width_shoulder
    point_f_y = point_e_y + height_shoulder
    point_fg_x = point_f_x
    point_fg_y = point_f_y + height_arm
    point_g_x = point_f_x + width_arm
    point_g_y = point_f_y + height_arm
    point_h_x = point_g_x + width_side
    point_h_y = point_g_y + height_side
    # Combine all the lines into one path
    path_d = " ".join([
        "M", str(point_a_x), str(point_a_y),  # Start (A)
        #where to start
        "L", str(point_b_x), str(point_b_y),  # Front Side Left (B) 1000 1400
        #could be in winkel
        "Q", str(point_bc_x), str(point_bc_y), str(point_c_x), str(point_c_y),  # Front Sleeve Hole Left (C)
        "L", str(point_d_x), str(point_d_y),  # Shoulder Front Right (D)
        "A", str(width_neckline/2) # radius x achse ellipse
            ,str(neckline_deep/2) # radius y achse ellipse
            ,"0 0 0",
        str(point_e_x), str(point_e_y),
        "L", str(point_f_x), str(point_f_y), #Shoulder right (F)
        "Q", str(point_fg_x), str(point_fg_y), str(point_g_x), str(point_g_y),  # Front Sleeve Hole right (G)
        "L", str(point_h_x), str(point_h_y), # Front Side Right
        "L", str(point_a_x), str(point_a_y)  # Front Hem
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
generate_tshirt_front_svg_cm(filename="curve.svg")  # Generate SVG with curved neckline
generate_tshirt_front_svg_cm(height_arm=40, filename="curve1.svg")  # Generate SVG with curved neckline
generate_tshirt_front_svg_cm(filename="curve2.svg")  # Generate SVG with curved neckline
generate_tshirt_front_svg_cm(filename="curve3.svg")  # Generate SVG with curved neckline


