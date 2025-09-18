import numpy as np
import cv2

cap = cv2.VideoCapture(1)

# Deaktiver RGB-konvertering i kamera hvis nødvendig
print(cap.set(cv2.CAP_PROP_CONVERT_RGB, 0))

# Definer grid-størrelse (juster etter behov)
grid_size = (8, 8)  # Antall rader og kolonner

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Cannot read frame.")
        break

    # Flat ut og vis data som uint16
    buffer = frame.flatten()
    buffer = buffer.view(np.uint16)

    # RAW12 til 8-bit konvertering
    buffer = buffer >> 4
    buffer = buffer.astype(np.uint8)

    # Bayer RAW til RGB-konvertering
    img_bayer = buffer.reshape((480, 640))  # Tilpass dimensjoner om nødvendig
    img = cv2.cvtColor(img_bayer, cv2.COLOR_BayerGBRG2RGB)

    # Bildebehandling for å finne hvite prikker
    lower_white = np.array([200, 200, 200])  # Juster terskel for hvitt lys
    upper_white = np.array([255, 255, 255])
    mask = cv2.inRange(img, lower_white, upper_white)

    # Finn konturer for de hvite områdene
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    light_positions = []  # Liste for lagring av lysposisjoner

    # Beregn cellestørrelser
    cell_width = img.shape[1] // grid_size[1]
    cell_height = img.shape[0] // grid_size[0]

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 10:  # Ignorer små støyområder
            continue

        # Beregn sirkel rundt hvite områder
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > 1:
            center = (int(x), int(y))
            radius = int(radius)

            # Beregn hvilken celle midtpunktet tilhører
            grid_col = center[0] // cell_width
            grid_row = center[1] // cell_height

            # Lagre grid-posisjonene
            light_positions.append((grid_col, grid_row))

            # Tegn sirkler og vis grid-koordinatene
            cv2.circle(img, center, radius, (0, 255, 0), 2)
            cv2.circle(img, center, 3, (0, 0, 255), -1)
            text = f"Cell ({grid_col}, {grid_row})"
            cv2.putText(img, text, (center[0] - 50, center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Vis resultatene
    cv2.imshow("Original Image with Detections", img)
    cv2.imshow("White Mask", mask)

    # Avslutt hvis 'q' trykkes
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
