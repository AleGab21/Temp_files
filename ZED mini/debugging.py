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
    numDisparities=16*15,  # Must be divisible by 16
    blockSize=13,  # Adjust for better noise reduction, can experiment with values like 9, 11, 15
    P1=8 * 3 * 13 ** 2,  # Penalty on disparity change, P1 and P2 are smoothness parameters
    P2=32 * 3 * 13 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=10,  # Low uniqueness for more accurate depth
    speckleWindowSize=100,  # Reduces speckles
    speckleRange=1,
    preFilterCap=31
)

# Distance calculation function
def calculate_distance(disparity, focal_length, baseline, x, y):
    d = disparity[y, x]
    if d > 0:
        depth = (focal_length * baseline) / d
    else:
        depth = float('inf')  # Infinite distance for zero disparity
    return depth

def calculate_median_distance(disparity, focal_length, baseline, x_start, x_end):
    heights, widths = disparity.shape
    distances = []
    for y in range(heights):
        for x in range(x_start, x_end):
            depth = calculate_distance(disparity, focal_length, baseline, x, y)
            if depth != float('inf'):
                distances.append(depth)
    if distances:
        return np.median(distances)
    else:
        return float('inf')

def map_distance_to_vibration(distance):
    if distance == float('inf'):
        return 0  # No vibration for infinite distance
    min_distance = 0.5  # Distance for maximum vibration
    max_distance = 5.0  # Distance for no vibration
    if distance <= min_distance:
        return 1  # Maximum vibration
    elif distance >= max_distance:
        return 0  # No vibration
    else:
        # Linear interpolation between min_distance and max_distance
        return 1 - (distance - min_distance) / (max_distance - min_distance)

focal_length = 736  # ZED Mini focal length in pixels for 720p resolution
baseline = 0.063  # Baseline for ZED Mini in meters

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    width = frame.shape[1] // 2
    frame_left = frame[:, :width]
    frame_right = frame[:, width:]

    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    disparity = stereo.compute(gray_left, gray_right).astype(np.float32) / 16.0

    # Apply a median filter to reduce noise
    disparity = cv2.medianBlur(disparity, 5)

    # Divide the disparity map into three sections
    section_width = disparity.shape[1] // 3
    left_distance = calculate_median_distance(disparity, focal_length, baseline, 0, section_width)
    middle_distance = calculate_median_distance(disparity, focal_length, baseline, section_width, 2 * section_width)
    right_distance = calculate_median_distance(disparity, focal_length, baseline, 2 * section_width, disparity.shape[1])

    # Map distances to vibration strengths
    left_vibration = map_distance_to_vibration(left_distance)
    middle_vibration = map_distance_to_vibration(middle_distance)
    right_vibration = map_distance_to_vibration(right_distance)

    print(f"Vibration strengths - Left: {left_vibration}, Middle: {middle_vibration}, Right: {right_vibration}")

    disparity_display = cv2.normalize(disparity, disparity, alpha=0, beta=300, norm_type=cv2.NORM_MINMAX)
    disparity_display = np.uint8(disparity_display)

    cv2.imshow("Left Camera", frame_left)
    cv2.imshow("Disparity map", disparity_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
