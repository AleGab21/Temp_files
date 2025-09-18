import os
import queue
import sounddevice as sd
import vosk
import json
import threading
import tkinter as tk
from tkinter import messagebox

mode = 0 

# Load the Vosk model (small, efficient offline model)
model_path = "vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    messagebox.showerror("Error", "Please download the Vosk model and unpack as 'vosk-model-small-en-us-0.15' in the current folder.")
    exit(1)

model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Setup microphone input
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def start_recognition():
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
                        
                        # Filter and display only specific commands
                        if "close range" in command:
                            command_label.config(text="Last Command: Close Range")
                            print("Command: Mode 1")
                            mode = 1
                        elif "indoors" in command:
                            command_label.config(text="Last Command: Inndoors")
                            print("Command: Mode 2")
                            mode = 2
                        elif "outdoors" in command:
                            command_label.config(text="Last Command: Outdoors")
                            print("Command: Mode 3")
                            mode = 3
                        else:
                            command_label.config(text="Last Command: None")
                            print("Command not recognized.")
                        
                        break  # Stop listening after recognizing a command
    
    threading.Thread(target=run).start()

# Create the main window
root = tk.Tk()
root.title("Speech Recognition App")

# Create a button to start the recognition
start_button = tk.Button(root, text="Start Recognition", command=start_recognition)
start_button.pack(pady=20)

# Create a label to display the last recognized command
command_label = tk.Label(root, text="Last Command: None")
command_label.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
