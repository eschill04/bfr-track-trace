# Read in an image and make binary mask with opencv

import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(filename):
    filename_no_ext = filename.split('.')[0]
    # Read in image
    img = cv2.imread(f'images/{filename}', cv2.IMREAD_COLOR)

    # Filter for red
    lower_red = np.array([0, 0, 200], dtype = "uint8")
    upper_red= np.array([200, 200, 255], dtype = "uint8")
    mask = cv2.inRange(img, lower_red, upper_red)

    # get points on edges
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    mask = np.zeros_like(mask)
    cv2.drawContours(mask, contours, 0, 255, -1)

    # approximate curve of contour as a spline
    plt.imshow(mask, cmap='gray')
    plt.show()

    # extract points on line
    points = np.where(mask == 255.0)
    points = np.array(points).T
    points = np.unique(points, axis=0)

    # save points to file
    np.savetxt(f'points/{filename_no_ext}.txt', points, fmt='%d')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-f", type=str, help="Filename of image to read")
    args = parser.parse_args()
    main(args.filename)