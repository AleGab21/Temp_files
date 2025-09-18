import cv2
import numpy as np

# Open stereo camera (ZED Mini outputs both left and right images side by side)
cap = cv2.VideoCapture(1)  # Assuming ZED Mini is the first camera

# Set the resolution (double width since it's a side-by-side image)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # 1280 * 2 (side-by-side)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Improved block matching for disparity with StereoSGBM
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=16*20,  # Must be divisible by 16
    blockSize=13,  # Adjust for better noise reduction, can experiment with values like 9, 11
    P1=8 * 3 * 13 ** 2,  # Penalty on disparity change, P1 and P2 are smoothness parameters
    P2=32 * 3 * 13 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=10,  # Low uniqueness for more accurate depth
    speckleWindowSize=100,  # Reduces speckles
    speckleRange=2,
    preFilterCap=31
)

# Distance calculation function
def calculate_distance(disparity, focal_length, baseline, x, y):
    # Calculate disparity
    d = disparity[y, x]
    if d > 0:
        depth = (focal_length * baseline) / d
    else:
        depth = float('inf')  # Infinite distance for zero disparity
    return depth

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        disparity = param['disparity']
        depth = calculate_distance(disparity, param['focal_length'], param['baseline'], x, y)
        print(f"Depth at ({x}, {y}): {depth:.2f} meters")

focal_length = 736  # ZED Mini focal length in pixels for 720p resolution
baseline = 0.063  # Baseline for ZED Mini in meters

cv2.namedWindow("Disparity map")
cv2.setMouseCallback("Disparity map", mouse_callback, {'focal_length': focal_length, 'baseline': baseline})

while True:
    # Capture stereo frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Split the frame into left and right images
    width = frame.shape[1] // 2
    frame_left = frame[:, :width]
    frame_right = frame[:, width:]

    # Convert to grayscale for disparity calculation
    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    # Calculate disparity map
    disparity = stereo.compute(gray_left, gray_right).astype(np.float32) / 16.0

    # Normalize disparity for display with higher contrast (grayscale)
    min_disp = 0  # Typically, this is 0 for disparity maps
    max_disp = stereo.getNumDisparities()  # Maximum disparity value based on stereo settings
    disparity_display = cv2.normalize(disparity, disparity, alpha=0, beta=300, norm_type=cv2.NORM_MINMAX)
    disparity_display = np.uint8(disparity_display)

    # Display frames
    cv2.imshow("Left Camera", frame_left)
    cv2.imshow("Disparity map", disparity_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Pass disparity map to mouse callback for depth calculations
    cv2.setMouseCallback("Disparity map", mouse_callback, {'disparity': disparity, 'focal_length': focal_length, 'baseline': baseline})

# Release resources
cap.release()
cv2.destroyAllWindows()
