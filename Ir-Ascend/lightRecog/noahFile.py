import numpy as np
from linuxpy.video.device import Device
import cv2  

def set_control_value(cam: Device, control_key: str, control_value: int):
    if cam.controls is None:
        print(f"Warning: Camera controls not available")
        return
    if control_key in cam.controls:
        cam.controls[control_key] = control_value
    else:
        print(f"Warning: Control \"{control_key}\" not available")
if __name__ == "__main__":
    cam = Device.from_id(4)
    cam.open()
    assert cam.controls is not None
    # Min/max can be queried with eg. cam.controls[...].min
    set_control_value(cam, "gain", 32)
    set_control_value(cam, "exposure_time_absolute", 600)
    for i, frame in enumerate(cam):
        if len(frame) == 0:
            print("Empty frame")
            continue
        buffer = frame.array
        buffer = buffer.view(np.uint16)
        # RAW12
        buffer = buffer >> 4
        # After shifting, all values are at most 255
        buffer = buffer.astype(np.uint8)
        img_bayer = buffer.reshape((frame.height, frame.width))
        img = cv2.cvtColor(img_bayer, cv2.COLOR_BayerGBRG2RGB)
        lower_white = np.array([100,100,100])
        upper_white = np.array([255,255,255])
        blur = cv2.GaussianBlur(img, (7,7), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(blur,lower_white,upper_white)
        res = cv2.bitwise_and(blur,blur,mask=mask)
        """
        edged = cv2.Canny(res,30,200)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        """
        cv2.imshow("iffi", res)
        if cv2.waitKey(5) == ord('q'):
            break
    cam.close()