import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from scipy.integrate import simps
from scipy.spatial import distance_matrix
import csv

FILENAME = '1'
SMOOTHING = 500

# Set to True to close the loop
# This will add a line connecting the last point to the first point
CLOSE_LOOP = True

# Read in points
points = np.loadtxt(f'points/{FILENAME}.txt')

# sort points by x
points = points[np.argsort(points[:, 1])]

x = points[:, 1]
y = points[:, 0]

x = x[::5]
y = y[::5]

points = np.column_stack((x, y))

# Function to find nearest neighbor path
def nearest_neighbor_path(points):
    n_points = len(points)
    visited = np.zeros(n_points, dtype=bool)
    path = [0]  # Start with the first point
    visited[0] = True

    for _ in range(1, n_points - 5):
        last_point = path[-1]
        dist = distance_matrix([points[last_point]], points)[0]
        dist[visited] = np.inf  # Ignore already visited points
        next_point = np.argmin(dist)
        path.append(next_point)
        visited[next_point] = True

    return path

# Get the nearest neighbor path
path_indices = nearest_neighbor_path(points)

# Reorder points based on the nearest neighbor path
x_sorted = points[path_indices][:, 0]
y_sorted = points[path_indices][:, 1]

if CLOSE_LOOP:
    x_sorted = np.append(x_sorted, x_sorted[0])
    y_sorted = np.append(y_sorted, y_sorted[0])

# Fit spline 
tck, u = splprep([x_sorted, y_sorted], s=SMOOTHING)
unew = np.linspace(0, 1, 1000)
out = splev(unew, tck)


print("Fitted!")


# Define a function to compute arc length between two points
def arc_length(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Define a function to compute the radius of curvature
def curvature(dx, dy, ddx, ddy):
    num = dx * ddy - dy * ddx
    denom = (dx**2 + dy**2)**(3/2)
    return num / denom if denom != 0 else np.inf  # Avoid division by zero

# Define a function to compute direction based on angle of the tangent
def direction_change(theta1, theta2):
    delta_theta = np.mod(theta2 - theta1, 2*np.pi)
    if delta_theta < np.pi:
        return "right"
    elif delta_theta > np.pi:
        return "left"
    else:
        return "straight"

# Number of points to evaluate the spline at
n_points = 1000
u_fine = np.linspace(0, 1, n_points)

# Generate the points and derivatives from the spline
x_fine, y_fine = splev(u_fine, tck)
dx_fine, dy_fine = splev(u_fine, tck, der=1)  # First derivatives
ddx_fine, ddy_fine = splev(u_fine, tck, der=2)  # Second derivatives

# Initialize lists to store data
arc_lengths = []
radii = []
directions = []

# Initial direction angle (in radians)
initial_theta = np.arctan2(dy_fine[0], dx_fine[0])

# Loop through each segment between spline points
for i in range(1, n_points):
    # Arc length
    length = arc_length(x_fine[i-1], y_fine[i-1], x_fine[i], y_fine[i])
    arc_lengths.append(length)

    # Radius of curvature (inverse of curvature)
    curve_radius = np.inf if curvature(dx_fine[i], dy_fine[i], ddx_fine[i], ddy_fine[i]) == 0 else 1 / np.abs(curvature(dx_fine[i], dy_fine[i], ddx_fine[i], ddy_fine[i]))
    radii.append(curve_radius)

    # Direction
    theta_i = np.arctan2(dy_fine[i], dx_fine[i])
    direction = direction_change(initial_theta, theta_i)
    directions.append(direction)

    # Update the initial direction angle
    initial_theta = theta_i

# Write to CSV file
with open(f'spline_data/{FILENAME}_spline_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Arc Length", "Radius of Curvature", "Direction"])

    # Write rows for each segment
    for i in range(n_points - 1):
        writer.writerow([arc_lengths[i], radii[i], directions[i]])

# Visualize spline from above

# Plot image
img = plt.imread(f'images/{FILENAME}.png')
plt.imshow(img, cmap='gray')

# Plot based on radii, arc length, and direction
for i in range(n_points - 1):
    color = 'r' if directions[i] == "right" else 'g' if directions[i] == "left" else 'b'
    plt.plot([x_fine[i], x_fine[i+1]], [y_fine[i], y_fine[i+1]], color)

# save images to results
plt.savefig(f'results/{FILENAME}_spline.png')

plt.show()

