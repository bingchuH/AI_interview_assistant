import time
import threading
import keyboard
from src.stt import MySpeechRecognitionListener, start_asr
from src.gpt_interaction import generate_response
import tkinter as tk
from src.transparent_log_window import TransparentLogWindow

def run_app(listener):
    # Start the speech recognition in a separate thread
    recognizer_thread = start_asr(listener)

    while listener.running:
        if keyboard.is_pressed('space'):
            listener.reset_text()
            print("Text reset.")
            time.sleep(0.02)  # prevent multiple detections
        elif keyboard.is_pressed('enter'):
            full_text = listener.get_full_text()
            print("Sending to ChatGPT...")
            response = generate_response(full_text)
            print("ChatGPT response:", response, "\n")
            listener.reset_text()
            time.sleep(0.02)  # prevent multiple detections
        elif keyboard.is_pressed('esc'):
            print("Exiting...")
            listener.running = False
            break

    recognizer_thread.join()
    del listener

def main():
    listener = MySpeechRecognitionListener(0)

    app_thread = threading.Thread(target=run_app, args=(listener,))
    app_thread.start()

    root = tk.Tk()
    app = TransparentLogWindow(root)
    root.mainloop()

    app_thread.join()

if __name__ == "__main__":
    main()
