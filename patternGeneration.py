def generate_tshirt_pattern_svg(width, sleeve_length, filename="tshirt_pattern.svg"):
    # Calculate coordinates based on input parameters
    front_curve_height = sleeve_length / 2

    # Create SVG pattern
    svg_pattern = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink" baseProfile="tiny" height="{sleeve_length * 3}" version="1.2" width="{width}">
  <defs/>
  <!-- Left Sleeve -->
  <path d="M {width / 5} {sleeve_length} Q {width / 4} {sleeve_length + sleeve_length / 4} {width / 3} {sleeve_length}" fill="rgb(255,217,194)" stroke="black"/>
  <!-- Right Sleeve -->
  <path d="M {width - (width / 5)} {sleeve_length} Q {width - (width / 4)} {sleeve_length + sleeve_length / 4} {width - (width / 3)} {sleeve_length}" fill="rgb(255,217,194)" stroke="black"/>
  <!-- Body Front -->
  <path d="M {width / 3} {sleeve_length} L {width - (width / 3)} {sleeve_length} Q {width - (width / 4)} {sleeve_length + front_curve_height} {width / 2} {sleeve_length * 2} Q {width / 4} {sleeve_length + front_curve_height} {width / 3} {sleeve_length}" fill="rgb(255,217,194)" stroke="black"/>
  <!-- Body Back -->
  <path d="M {width / 3} {sleeve_length} L {width - (width / 3)} {sleeve_length} Q {width - (width / 4)} {sleeve_length + front_curve_height} {width / 2} {sleeve_length * 2} Q {width / 4} {sleeve_length + front_curve_height} {width / 3} {sleeve_length}" fill="rgb(255,217,194)" stroke="black"/>
  <!-- Labels -->
  <text fill="rgb(9,33,173)" font-size="25" x="{width / 5}" y="{sleeve_length + 30}">Left Sleeve</text>
  <text fill="rgb(9,33,173)" font-size="25" x="{width - (width / 5)}" y="{sleeve_length + 30}">Right Sleeve</text>
  <text fill="rgb(9,33,173)" font-size="25" x="{width / 2 - 50}" y="{sleeve_length * 2 + 30}">Body Front</text>
  <text fill="rgb(9,33,173)" font-size="25" x="{width / 2 - 50}" y="{sleeve_length * 2 + 30}">Body Back</text>
</svg>"""

    # Save SVG pattern to file
    with open(filename, "w") as f:
        f.write(svg_pattern)

    print(f"SVG pattern saved to {filename}")

# Example usage:
width = 1000
sleeve_length = 150
generate_tshirt_pattern_svg(width, sleeve_length, filename="tshirt_pattern.svg")