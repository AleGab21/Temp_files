import cv2
import numpy as np

def detect_white_dots(image_path, output_path=None):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Error: Image not found.")
        return

    # Threshold the image to binary (white dots on black background)
    _, binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    # Find contours of the white dots
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw circles around detected dots (optional)
    result = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for contour in contours:
        # Get the center and radius of a minimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(result, center, radius, (0, 255, 0), 2)  # Draw the circle in green

    # Display the result
    cv2.imshow("Detected White Dots", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the result if an output path is provided
    if output_path:
        cv2.imwrite(output_path, result)

# Example usage
image_path = "C:\\Users\\alex_\\OneDrive\\Skrivebord\\Ascend\\polka.jpg"
output_path = "C:\\Users\\alex_\\OneDrive\\Skrivebord\\Ascend"
detect_white_dots(image_path, output_path)
