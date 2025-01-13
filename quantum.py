import math
from typing import List, Tuple

def generate_hatch_pattern(width: float, height: float, angle_degrees: float, spacing: float) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Generate a list of line segments that form a hatch pattern over a rectangle.
    
    Args:
        width: Width of the rectangle
        height: Height of the rectangle
        angle_degrees: Angle of the hatch lines in degrees (0-180)
        spacing: Distance between parallel hatch lines
        
    Returns:
        List of line segments, where each segment is a tuple of two points ((x1,y1), (x2,y2))
    """
    # Convert angle to radians and normalize to 0-180 degrees
    angle = math.radians(angle_degrees % 180)
    
    # Handle special cases of vertical and horizontal lines
    if angle_degrees % 180 == 0:
        return _generate_vertical_lines(width, height, spacing)
    elif angle_degrees % 180 == 90:
        return _generate_horizontal_lines(width, height, spacing)
    
    # Calculate the normal vector to the hatch lines
    normal_x = math.cos(angle + math.pi/2)
    normal_y = math.sin(angle + math.pi/2)
    
    # Calculate the direction vector of the hatch lines
    dir_x = math.cos(angle)
    dir_y = math.sin(angle)
    
    # Find the corners of the rectangle
    corners = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height)
    ]
    
    # Project corners onto the normal vector to find the range of the pattern
    projections = [normal_x * x + normal_y * y for x, y in corners]
    min_proj = min(projections)
    max_proj = max(projections)
    
    # Generate parallel lines
    lines = []
    current_proj = min_proj
    while current_proj <= max_proj:
        # Calculate a point on the current line
        point_on_line_x = normal_x * current_proj
        point_on_line_y = normal_y * current_proj
        
        # Find intersections with rectangle edges
        intersections = []
        
        # Check intersections with horizontal edges
        for y in [0, height]:
            # Solve: point + t * dir = (x, y)
            t = (y - point_on_line_y) / dir_y if dir_y != 0 else float('inf')
            x = point_on_line_x + t * dir_x
            if 0 <= x <= width:
                intersections.append((x, y))
                
        # Check intersections with vertical edges
        for x in [0, width]:
            # Solve: point + t * dir = (x, y)
            t = (x - point_on_line_x) / dir_x if dir_x != 0 else float('inf')
            y = point_on_line_y + t * dir_y
            if 0 <= y <= height:
                intersections.append((x, y))
        
        # If we found exactly 2 intersections, add the line
        if len(intersections) >= 2:
            # Sort intersections to ensure consistent line direction
            intersections.sort()
            lines.append((intersections[0], intersections[1]))
        
        current_proj += spacing
    
    return lines

def _generate_vertical_lines(width: float, height: float, spacing: float) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Generate vertical lines for the hatch pattern."""
    lines = []
    x = 0
    while x <= width:
        lines.append(((x, 0), (x, height)))
        x += spacing
    return lines

def _generate_horizontal_lines(width: float, height: float, spacing: float) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """Generate horizontal lines for the hatch pattern."""
    lines = []
    y = 0
    while y <= height:
        lines.append(((0, y), (width, y)))
        y += spacing
    return lines
