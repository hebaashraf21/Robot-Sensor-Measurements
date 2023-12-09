import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Function to calculate the endpoint of a ray given start point, angle, and max range
def get_end_point(start_point, angle, max_range):
    x, y = start_point
    end_x = x + max_range * np.cos(angle * np.pi / 180)
    end_y = y + max_range * np.sin(angle * np.pi / 180)
    return int(end_x), int(end_y)

# Function to validate user inputs based on map size
def validate_input(x, y, theta, map_width, map_height):
    if not (0 <= x < map_width and 0 <= y < map_height):
        raise ValueError("Robot x and y coordinates must be within the bounds of the map. (680,400)")

# Function to cast rays through the map and visualize them on the image
def cast_rays(robot_pose, opening_angle, max_range, map_path, map_width, map_height, output_file):
    # Read the map image using cv2
    map_array = cv2.imread(map_path)

    # Extract robot pose information
    x, y, theta = robot_pose

    # Draw the robot
    robot_radius = 6 
    circle = Circle((robot_pose[0], robot_pose[1]), robot_radius, color='red')
    plt.gca().add_patch(circle)

    # Plot the robot orientation as a line
    plt.plot(
        [robot_pose[0], robot_pose[0] + 50 * np.cos(robot_pose[2] * np.pi / 180)], 
        [robot_pose[1], robot_pose[1] + 50 * np.sin(robot_pose[2] * np.pi / 180)], 
        color='black')

    # Convert robot coordinates to map coordinates
    start_point = (int(x), int(y))

    # Create a list to store measurements
    measurements = []

    # Iterate over angles within the specified opening angle
    for angle in range(int(theta) - opening_angle // 2, int(theta) + opening_angle // 2 + 1, 2):

        # Loop over the points of each line
        laser_range, laser_step = max_range, 1
        max_distance = 0
        endpoint = None
        for d in range(0, int(laser_range), laser_step):
            # Calculate the endpoint of the ray
            end_point = get_end_point(start_point, angle, d)

            # Check if the point corresponds to a black pixel in the map
            if (np.linalg.norm(map_array[end_point[1], end_point[0]] - np.array([0, 0, 0])) == 0):
                d = laser_range
                break  # Break the loop if a black pixel is encountered
            else:
                # Update the maximum distance and endpoint for the angle
                max_distance = d
                endpoint = end_point

                # Draw the green ray by setting the pixel color to [0, 255, 0]
                map_array[end_point[1], end_point[0]] = [0, 255, 0]

        # Save the measurements
        measurements.append((angle, endpoint, max_distance))

    # Save measurements to a text file
    with open(output_file, 'w') as file:
        file.write("Angle\tEndpoint\tMax_Distance\n")
        for angle, endpoint, max_distance in measurements:
            file.write(f"{angle}\t{endpoint}\t{max_distance}\n")

    # Display the map with the drawn rays using Matplotlib
    plt.imshow(cv2.cvtColor(map_array, cv2.COLOR_BGR2RGB))
    plt.show()

# Define map size
map_width = 680
map_height = 400

# Take robot pose as input from the user with validation
try:
    x = float(input("Enter the x-coordinate of the robot: "))
    y = float(input("Enter the y-coordinate of the robot: "))
    theta = float(input("Enter the orientation (theta) of the robot in degrees: "))
    validate_input(x, y, theta, map_width, map_height)
except ValueError as e:
    print(f"Invalid input: {e}")
else:
    robot_pose = (x, y, theta)

    opening_angle = 250
    max_range = 1200 / 4
    map_path = "Map.jpg"
    output_file = "measurements.txt"

    # Cast the rays and save measurements
    cast_rays(robot_pose, opening_angle, max_range, map_path, map_width, map_height, output_file)
