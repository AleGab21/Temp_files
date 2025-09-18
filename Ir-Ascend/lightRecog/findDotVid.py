import numpy as np
import cv2

cap = cv2.VideoCapture(1)

# Deaktiver RGB-konvertering i kamera hvis nødvendig
print(cap.set(cv2.CAP_PROP_CONVERT_RGB, 0))

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
    lower_white = np.array([40, 40, 40])  # Juster terskel for hvitt lys
    upper_white = np.array([255, 255, 255])
    mask = cv2.inRange(img, lower_white, upper_white)  # Lag maske for hvite områder

    # Finn konturer for de hvite områdene
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 10:  # Ignorer små støyområder
            continue

        # Beregn sirkel rundt hvite områder
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius > 1:  # Filtrer basert på radius
            center = (int(x), int(y))
            radius = int(radius)

            # Tegn grønn sirkel rundt konturen
            cv2.circle(img, center, radius, (0, 255, 0), 2)

            # Tegn rød prikk i midten av konturen
            cv2.circle(img, center, 3, (0, 0, 255), -1)  # Rød prikk (radius 3)

    # Vis resultatene
    cv2.imshow("Original Image with Detections", img)
    cv2.imshow("White Mask", mask)

    # Avslutt hvis 'q' trykkes
    if cv2.waitKey(5) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
