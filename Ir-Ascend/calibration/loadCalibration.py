import cv2
import numpy as np

# Load the calibration data
mtx = np.load("camera_matrix.npy")
dist = np.load("dist_coeff.npy")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

    # Apply undistortion
    undistorted_frame = cv2.undistort(frame, mtx, dist, None, new_camera_mtx)

    cv2.imshow("Original", frame)
    cv2.imshow("Undistorted", undistorted_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
