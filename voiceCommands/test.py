import os
import queue
import sounddevice as sd
import vosk
import json

# Load the Vosk model (small, efficient offline model)
model_path = "vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print("Please download the Vosk model and unpack as 'vosk-model-small-en-us-0.15' in the current folder.")
    exit(1)

model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Setup microphone input
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Initialize microphone stream
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
                
                # Test simple command translation
                if "take off" in command:
                    print("Command: Take Off")
                elif "land" in command:
                    print("Command: Land")
                elif "move forward" in command:
                    print("Command: Move Forward")
                else:
                    print("Command not recognized.")
