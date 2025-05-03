import sounddevice as sd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time


cancel_shutdown = False

def show_warning_and_shutdown():
    global cancel_shutdown
    cancel_shutdown = False

 
    def on_cancel():
        global cancel_shutdown
        cancel_shutdown = True
        root.destroy()

    root = tk.Tk()
    root.title("Too Noisy!")
    root.geometry("350x100")
    root.resizable(False, False)
    root.attributes('-topmost', True)

    label = tk.Label(root, text="SHUT UP BITCH!!! PC will shut down in 3 seconds.", padx=10, pady=10)
    label.pack()

    cancel_button = tk.Button(root, text="Cancel", command=on_cancel, width=10)
    cancel_button.pack(pady=5)

    def auto_shutdown():
        time.sleep(3)
        if not cancel_shutdown:
            root.destroy()
            os.system("shutdown /s /t 0")

    Thread(target=auto_shutdown, daemon=True).start()
    root.mainloop()

def monitor_noise(threshold=0.2):  
    def callback(indata, frames, time_info, status):
        volume = np.sqrt(np.mean(indata**2))
        print(f"Volume: {volume:.4f}")  

        if volume > threshold:
            print("LOUD NOISE DETECTED!")
            Thread(target=show_warning_and_shutdown).start()

    with sd.InputStream(callback=callback, channels=1, samplerate=44100):
        sd.sleep(1000000)



monitor_noise()
