# Read in an image and make binary mask with opencv

import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

def get_scale(img):
    # identify grid lines of image, and calculate scale of pixels per square
    # return scale

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # get vertical and horizontal edges
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    # display edges
    plt.imshow(lines, cmap='gray')

    # approximate curve of contour as a spline
    plt.show()

    

def main(filename):
    filename_no_ext = filename.split('.')[0]
    # Read in image
    img = cv2.imread(f'images/{filename}', cv2.IMREAD_COLOR)

    # get scale of image
    get_scale(img)

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