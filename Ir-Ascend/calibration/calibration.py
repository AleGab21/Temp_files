import cv2
import numpy as np
import time

# Grid settings
grid_size = (4, 5)  # Adjust to match your IR LED grid
led_spacing = 0.1  # Distance between LEDs in meters (10cm)

# Generate object points based on grid size and spacing
objp = np.zeros((grid_size[0] * grid_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:grid_size[1], 0:grid_size[0]].T.reshape(-1, 2) * led_spacing

#print(objp)
# Storage for calibration points
objpoints = []  # 3D world coordinates
imgpoints = []  # 2D detected points

# Open the camera
cap = cv2.VideoCapture(1)  # Adjust index if needed
cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

# Configure IR blob detector
blob_params = cv2.SimpleBlobDetector_Params()
blob_params.filterByArea = True
blob_params.filterByCircularity = True
blob_params.minArea = 10  # Adjust based on LED size
blob_params.maxArea = 10000
blob_params.filterByConvexity = False
blob_params.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(blob_params)

# Instructions
print("Press 'SPACE' to start calibration.")
print("Point the camera at the IR LED grid.")

def convert_frame(frame):
    height, width = frame.shape
    buffer = frame.flatten()
    buffer = buffer.view(np.uint16)
    buffer = buffer >> 4
    buffer = buffer.astype(np.uint8)
    img_bayer = buffer.reshape((480, 640))
    return cv2.cvtColor(img_bayer, cv2.COLOR_BayerGBRG2BGR)

def findMines(img):
       # Bildebehandling for å finne hvite prikker
    lower_white = np.array([200])  # Juster terskel for hvitt lys
    upper_white = np.array([255])
    mask = cv2.inRange(img, lower_white, upper_white)

    # Finn konturer for de hvite områdene
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    light_positions = []  # Liste for lagring av lysposisjoner

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 10:  # Ignorer små støyområder
            continue

        # Beregn sirkel rundt hvite områder
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > 1:  # Filtrer basert på radius
            center = (int(x), int(y))
            radius = int(radius)

            # Lagre pikselkoordinatene
            #print(x,y)
            light_positions.append(cv2.KeyPoint(x, y, radius*2))
    bins = [[] for _ in range(grid_size[0])]

    light_positions.sort(key=lambda point: point.pt[1])
    bin_index = 0
    for i in range(0, len(light_positions), grid_size[1]):
        bins[bin_index].extend(light_positions[i:i+grid_size[1]])
        bin_index += 1

    for bin_index in range(len(bins)):
        bins[bin_index].sort(key=lambda point: point.pt[0])

    return [point for bin in bins for point in bin]

""""
while True:
    _, frame = cap.read()
    frame = convert_frame(frame)
    cv2.imshow("Live Feed", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):  # Press SPACE to start
        break
"""
print("\nCalibration started! Follow the instructions in the terminal.")
print("Hold the camera still when instructed. A countdown will appear.")

positions = [
    "Hold still at the center and press SPACE to capture.", 
    "Move the grid slightly left, then return to center.", 
    "Move the grid slightly right, then return to center.", 
    "Tilt the grid up, then return to center.", 
    "Tilt the grid down, then return to center."
]

captured_images = 0
while captured_images < len(positions):

    #for i in range(3, 0, -1):  # Countdown before capture
    #    print(i)
    #    time.sleep(1)

    ret, frame = cap.read()
    frame = convert_frame(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    keypoints = findMines(gray)

    # Display detected LEDs
    img_with_keypoints = cv2.drawKeypoints(gray, keypoints, None, (0, 255, 0),
                                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    blue = 255
    red = 0
    for point1, point2 in zip(keypoints, keypoints[1:]):
        cv2.line(img_with_keypoints, tuple(map(int,point1.pt)), tuple(map(int,point2.pt)), (blue,0,red))
        blue -= 20
        red += 20

    cv2.imshow("Detected IR LEDs", img_with_keypoints)

    key = cv2.waitKey(1) & 0xFF
    if key != ord(' '):  # Press SPACE to start
        continue
    print(f"\n{positions[captured_images]}")
    print("Hold the position! Capturing in:")

    

    if len(keypoints) == grid_size[0] * grid_size[1]:  # Ensure correct number of LEDs detected
        imgp = np.array([kp.pt for kp in keypoints], dtype=np.float32)
        objpoints.append(objp)
        imgpoints.append(imgp)
        captured_images += 1
        
        print("Captured!")
    

    else:
        print("Error: Could not detect the full LED grid. Try adjusting the position.")

cap.release()
cv2.destroyAllWindows()

# Perform camera calibration if enough valid images were captured
if len(objpoints) > 3:  # Minimum images needed for calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    print("\nCalibration successful! Saving data...")
    np.save("camera_matrix.npy", mtx)
    np.save("dist_coeff.npy", dist)

    print("Camera Matrix:\n", mtx)
    print("Distortion Coefficients:\n", dist)
    print("\nCalibration data saved! You can now use this for improved accuracy.")

else:
    print("Calibration failed. Not enough valid images.")

