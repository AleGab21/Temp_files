import cv2
import numpy as np

# open stereo camera (ZED Mini outputs both left and right images side by side)
cap = cv2.VideoCapture(1)  # Assuming ZED Mini is the first camera

# Set the resolution (double width since it's a side-by-side image)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)  # 1280 * 2 (side-by-side)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# block matching for disparity
stereo = cv2.StereoBM_create(numDisparities=192, blockSize=5)

# distance calculation
def calculate_distance(disparity, focal_length, baseline, x, y):
    # calculate disparity
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
baseline = 0.064  # Baseline for ZED Mini in meters

cv2.namedWindow("Disparity map")
cv2.setMouseCallback("Disparity map", mouse_callback, {'focal_length': focal_length, 'baseline': baseline})

while True:
    # capture stereo frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # split the frame into left and right images
    width = frame.shape[1] // 2
    frame_left = frame[:, :width]
    frame_right = frame[:, width:]

    # converting to grayscale for disparity calculation
    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    # calculate disparity map
    disparity = stereo.compute(gray_left, gray_right).astype(np.float32) / 16.0
    disparity_display = cv2.normalize(disparity, disparity, alpha=20, beta=700, norm_type=cv2.NORM_MINMAX)
    disparity_display = np.uint8(disparity_display)

    # display frames
    cv2.imshow("Left Camera", frame_left)
    cv2.imshow("Disparity map", disparity_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # pass disparity map to mouse callback for depth calculations
    cv2.setMouseCallback("Disparity map", mouse_callback, {'disparity': disparity, 'focal_length': focal_length, 'baseline': baseline})

# release resources
cap.release()
cv2.destroyAllWindows()
