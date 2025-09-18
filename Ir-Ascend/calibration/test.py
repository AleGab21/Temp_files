import numpy as np
import cv2

# Load saved calibration data
mtx = np.load("camera_matrix.npy")
dist = np.load("dist_coeff.npy")

# Load an image to undistort
img = cv2.imread("test_image.jpg")
h, w = img.shape[:2]
new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# Undistort
undistorted_img = cv2.undistort(img, mtx, dist, None, new_camera_mtx)

cv2.imshow("Undistorted Image", undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
