import os
import queue
import sounddevice as sd
import vosk
import json
import threading
import RPi.GPIO as GPIO  

# sett opp GPIO for knapp
BUTTON_PIN = 18  # GPIO pin 
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mode = 0  # mode

# last inn Vosk model
model_path = "vosk-model-small-en-us-0.15"

if not os.path.exists(model_path):
    print("Error: Please download the Vosk model and unpack as 'vosk-model-small-en-us-0.15' in the current folder.")
    exit(1)

model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Setup microfon 
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def start_recognition():
    global mode
    def run():
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            print("Listening... Speak into the microphone.")
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    if "text" in result:
                        command = result['text']
                        print(f"Recognized: {command}")
                        
                        # Filter commandoer og mode valg
                        if "close range" in command:
                            mode = 1
                            print("Mode set to 1 (Close Range)")
                        elif "indoors" in command:
                            mode = 2
                            print("Mode set to 2 (Indoors)")
                        elif "outdoors" in command:
                            mode = 3
                            print("Mode set to 3 (Outdoors)")
                        else:
                            mode = 0
                            print("Command not recognized, mode set to 0")
                        
                        break  # Stop microfon 
    
    threading.Thread(target=run).start()

def button_pressed(channel):
    """Callback function when the button is pressed."""
    print("Button pressed! Starting speech recognition...")
    start_recognition()

# interupt for knapp 
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

print("System ready. Press the button to start speech recognition.")

try:
    # For å se etter knappetrykk
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    GPIO.cleanup()  
