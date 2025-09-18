import usb.core
import usb.util

# Find the ZED Mini camera or any other device (adjust the IDs if known)
dev = usb.core.find()

if dev is None:
    print("Device not found.")
else:
    try:
        # Print out the serial number
        serial_number = usb.util.get_string(dev, dev.iSerialNumber)
        print(f"Serial Number: {serial_number}")
    except usb.core.USBError as e:
        print(f"Error: {e}")
    except AttributeError:
        print("Serial number attribute not found.")

        #10027838
