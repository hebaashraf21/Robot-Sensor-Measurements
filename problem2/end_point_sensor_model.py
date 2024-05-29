import os
import cv2
import numpy as np

def calculate_likelihood_field(binary_map, sigma):
    # Compute the distance transform
    distance_transform = cv2.distanceTransform(binary_map, cv2.DIST_L2, 0)

    # Apply a Gaussian likelihood model
    likelihood_field = 1.0 / (np.sqrt(2 * np.pi * sigma)) * np.exp(-0.5 * ((distance_transform / sigma)**2))

    # Normalize the likelihood field
    likelihood_field = cv2.normalize(likelihood_field, None, 0, 1, cv2.NORM_MINMAX)

    return likelihood_field

def endpoint_model(map_image_path, save_likelihood_field_path, save_probability_map_path, max_ray, sigma):
    # Read the map image
    map_image = cv2.imread(map_image_path, cv2.IMREAD_GRAYSCALE)

    # Binarize the image using Otsu's thresholding
    _, binary_map = cv2.threshold(map_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Calculate likelihood field
    likelihood_field = calculate_likelihood_field(binary_map, sigma)

    # Save the likelihood field image
    cv2.imwrite(save_likelihood_field_path, (likelihood_field * 255).astype(np.uint8))

    # Initialize the probability map
    probability_map = np.zeros_like(map_image, dtype=np.float32)

    # Loop over pixels
    for x in range(likelihood_field.shape[1]):
        for y in range(likelihood_field.shape[0]):
            max_probability = 0.0

            # Loop over angles (θ)
            for theta in range(0, 360, 1):
                # Compute ray endpoints
                endpoint_x = int(x + (max_ray*100/4) * np.cos(theta * np.pi / 180))
                endpoint_y = int(y + (max_ray*100/4) * np.sin(theta * np.pi / 180))

                # Check map bounds
                if 0 <= endpoint_x < map_image.shape[1] and 0 <= endpoint_y < map_image.shape[0]:
                    # Compute probability
                    probability = likelihood_field[endpoint_y, endpoint_x]

                    # Store maximum probability
                    max_probability = max(max_probability, probability)

            # Store the maximum probability in the probability map
            probability_map[y, x] = max_probability

    # Save the probability map image
    cv2.imwrite(save_probability_map_path, (probability_map * 255).astype(np.uint8))

    # Return the computed probability map
    return probability_map

# Example usage
map_image_path = "Map.jpg"
output_folder = "output/"
os.makedirs(output_folder, exist_ok=True)

# Define test cases
test_cases = [

    {"sigma": 1, "max_ray": 0.1},
    {"sigma": 5, "max_ray": 0.1},
    {"sigma": 15, "max_ray": 0.1},
    {"sigma": 20, "max_ray": 0.1},
    {"sigma": 1, "max_ray": 0.5},
    {"sigma": 5, "max_ray": 0.5},
    {"sigma": 15, "max_ray": 0.5},
    {"sigma": 20, "max_ray": 0.5},
    {"sigma": 1, "max_ray": 0.8},
    {"sigma": 5, "max_ray": 0.8},
    {"sigma": 15, "max_ray": 0.8},
    {"sigma": 20, "max_ray": 0.8},
    {"sigma": 1, "max_ray": 1},
    {"sigma": 5, "max_ray": 1},
    {"sigma": 15, "max_ray": 1},
    {"sigma": 20, "max_ray": 1},
    {"sigma": 1, "max_ray": 2},
    {"sigma": 5, "max_ray": 2},
    {"sigma": 15, "max_ray": 2},
    {"sigma": 20, "max_ray": 2},
    {"sigma": 1, "max_ray": 3},
    {"sigma": 5, "max_ray": 3},
    {"sigma": 15, "max_ray": 3},
    {"sigma": 20, "max_ray": 3},


]

# Loop through test cases
for idx, test_case in enumerate(test_cases, start=1):
    print(idx)
    sigma = test_case["sigma"]
    max_ray = test_case["max_ray"]
    
    save_likelihood_field_path = f"{output_folder}likelihood_field_sigma_{sigma}.jpg"
    save_probability_map_path = f"{output_folder}probability_map_sigma_{sigma}_max_ray_{max_ray}.jpg"

    probability_map = endpoint_model(map_image_path, save_likelihood_field_path, save_probability_map_path, max_ray, sigma)
