# Read in an image and make binary mask with opencv

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read in image
img = cv2.imread('images/1.png', cv2.IMREAD_COLOR)

# Filter for red
lower_red = np.array([0, 0, 200], dtype = "uint8")
upper_red= np.array([200, 200, 255], dtype = "uint8")
mask = cv2.inRange(img, lower_red, upper_red)


# Get largest contour
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea, reverse = True)
mask = np.zeros_like(mask)
cv2.drawContours(mask, contours, 0, 255, -1)

# Display mask
plt.imshow(mask)
plt.show()

# extract points on line
points = np.where(mask == 255.0)
points = np.array(points).T
print(points)
print(points.shape)

# save points to file
np.savetxt('points.txt', points, fmt='%d')
