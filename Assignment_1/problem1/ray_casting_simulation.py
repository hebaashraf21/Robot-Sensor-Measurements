import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Function to calculate the endpoint of a ray given start point, angle, and max range
def get_end_point(start_point, angle, max_range):
    x, y = start_point
    rad_angle = np.radians(angle)
    end_x = x + max_range * np.cos(rad_angle)
    end_y = y + max_range * np.sin(rad_angle)
    return int(end_x), int(end_y)

# Function to retrieve points on a line using Bresenham's line algorithm
def get_points_on_line(start_point, end_point):
    x0, y0 = start_point
    x1, y1 = end_point

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    points = []

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

    return points

# Function to cast rays through the map and visualize them on the image
def cast_rays(robot_pose, opening_angle, max_range, map_path):
    # Read the map image using cv2
    map_array = cv2.imread(map_path)

    # Extract robot pose information
    x, y, theta = robot_pose
    # Convert robot coordinates to map coordinates (assuming each pixel is 4cm x 4cm)
    start_point = (robot_pose[0], robot_pose[1])
    
     # Draw the robot as a red circle
    robot_radius = 6 # Adjust the radius as needed
    circle = Circle((start_point[0], start_point[1]), robot_radius, color='red')
    plt.gca().add_patch(circle)

    # Iterate over angles within the specified opening angle
    for angle in range(theta - opening_angle // 2, theta + opening_angle // 2 + 1, 2):
        # Calculate the endpoint of the ray
        end_point = get_end_point(start_point, angle, max_range)
        # Get all points on the line using Bresenham's algorithm
        line_points = get_points_on_line(start_point, end_point)

      # Iterate over points on the line
        for point in line_points:
            px, py = point

            # Calculate the distance from the start point to the current point
            distance = np.linalg.norm(np.array(point) - np.array(start_point))

            # Check if the distance exceeds the max range
            if distance > max_range:
                break  # Break the loop if the max range is exceeded

            # Check if the point is within the map boundaries
            if px >= 0 and px < map_array.shape[1] and py >= 0 and py < map_array.shape[0]:
                # Check if the point corresponds to a black pixel in the map
                if np.linalg.norm(map_array[py, px] - np.array([0, 0, 0])) == 0:
                    break  # Break the loop if a black pixel is encountered
                else:
                    # Draw the green ray by setting the pixel color to [0, 255, 0]
                    map_array[py, px] = [0, 255, 0]

    # Display the map with the drawn rays using Matplotlib
    plt.imshow(cv2.cvtColor(map_array, cv2.COLOR_BGR2RGB))
    plt.show()

# Example usage:
robot_pose = (350, 170, 190)  # (x, y, theta)
opening_angle = 250
max_range = 1200  # 12m in 4cm units
map_path = "Map.jpg"  # Update with the actual path to your map
cast_rays(robot_pose, opening_angle, max_range, map_path)
