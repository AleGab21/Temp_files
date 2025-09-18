import os
import queue
import sounddevice as sd
import vosk
import json
import threading
import tkinter as tk
from tkinter import messagebox

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
                        if "take off" in command:
                            command_list.insert(tk.END, "Take Off")
                            print("Command: Take Off")
                        elif "land" in command:
                            command_list.insert(tk.END, "Land")
                            print("Command: Land")
                        elif "move forward" in command:
                            command_list.insert(tk.END, "Move Forward")
                            print("Command: Move Forward")
                        else:
                            command_list.insert(tk.END, "Command not recognized")
                            print("Command not recognized.")
                        
                        break  # Stop listening after recognizing a command
    
    threading.Thread(target=run).start()

# Create the main window
root = tk.Tk()
root.title("Speech Recognition App")

# Create a button to start the recognition
start_button = tk.Button(root, text="Start Recognition", command=start_recognition)
start_button.pack(pady=20)

# Create a listbox to display the recognized commands
command_list = tk.Listbox(root)
command_list.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
