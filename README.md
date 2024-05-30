# Sensor Models

## Overview
This repository contains the solution for CMP2024 Robotics course Assignment 1, focusing on sensor models for laser-range measurements and their likelihood fields. The assignment involves generating laser-range measurements using ray casting and implementing the endpoint model for these measurements.<br>

## Problem 1

**Objective:** Generate laser-range measurements for a given robot pose (x, y, θ) on a 2D grid-map using ray casting.<br>

**Method:**<br>

1. A map image is loaded using OpenCV.
2. Laser-range measurements are generated for an opening angle of 250° (125° left and right of the heading direction) with measurements taken every 2°.<br>
3. The endpoint of each laser ray is determined by checking for obstacles within a maximum range of 12 meters (converted to pixels).<br>
4. The measurements, including endpoints and distances for each angle, are saved in the measurements.txt file.<br>
5. The map with drawn rays is displayed using Matplotlib.<br>

**Code Explanation:**<br>

- The get_end_point function calculates the endpoint of a ray given the start point, angle, and maximum range.<br>
- The validate_input function ensures the robot's pose is within the bounds of the map.<br>
- The cast_rays function performs ray casting, stores measurements, and visualizes the results on the map.<br>

**Figures**<br>

Pose 1: (x = 350, y = 190, θ = 90°)<br>
<img src="assets/cast1.png" alt=" " ><br>
Pose 2: (x = 30, y = 190, θ = 50°)<br>
<img src="assets/cast2.png" alt=" " ><br>
The measurements, including endpoints and distances for each angle, are saved in the measurements.txt file.<br>

## Problem 2
**Objective:** Implement the endpoint model for laser-range measurements and compute the likelihood field for different sigma values and maximum ray lengths.<br>

**Method:**<br>
1. The map image is binarized using Otsu's thresholding.<br>
2. A likelihood field is computed using a Gaussian model applied to the distance transform of the binary map.<br>
3. For each cell in the map, the maximum likelihood over all orientations is computed and visualized as a grayscale value.<br>
4. The results for different sigma values and maximum ray lengths are saved as images.<br>

**Code Explanation:**<br>
-The calculate_likelihood_field function computes the likelihood field using a Gaussian model.<br>
- The endpoint_model function calculates the probability map for different sigma values and maximum ray lengths and saves the results as images.<br>
  
1. Likelihood Field at Different Sigmas:<br>
<img src="assets/sigmas.png" alt=" " ><br>
2. Probability Map at Different Sigmas and Max_ray Values:<br>
Sigma = 1<br>
<img src="assets/sigma_1_1.png" alt=" " width="48%"> <img src="assets/sigma_1_2.png" alt=" " width="48%"><br>
Sigma = 5<br>
<img src="assets/sigma_5_1.png" alt=" " width="48%"> <img src="assets/sigma_5_2.png" alt=" " width="48%"><br>
Sigma = 15<br>
<img src="assets/sigma_15_1.png" alt=" " width="48%"> <img src="assets/sigma_15_2.png" alt=" " width="48%"><br>
Sigma = 20<br>
<img src="assets/sigma_20_1.png" alt=" " width="48%"> <img src="assets/sigma_20_2.png" alt=" " width="48%"><br>
