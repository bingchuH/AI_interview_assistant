import tkinter as tk
from tkinter import ttk
import sys

class TransparentLogWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Transparent Log Window")

        # Make the window transparent
        self.root.attributes('-alpha', 0.5)
        # Remove window borders
        self.root.overrideredirect(True)
        # Keep the window always on top
        self.root.attributes('-topmost', 1)

        # Create a draggable area
        self.frame = ttk.Frame(self.root, relief='solid', padding=10)
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.frame.bind("<ButtonPress-1>", self.start_move)
        self.frame.bind("<ButtonRelease-1>", self.stop_move)
        self.frame.bind("<B1-Motion>", self.do_move)

        # Create a scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add a text area to the frame and link it to the scrollbar
        self.text = tk.Text(self.frame, wrap='word', bg='white', fg='black', borderwidth=1, font=('Helvetica', 12), yscrollcommand=self.scrollbar.set)
        self.text.pack(expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.text.yview)

        # Create a close button
        self.close_button = ttk.Button(self.frame, text="X", command=self.root.destroy)
        self.close_button.place(relx=1.0, rely=0.0, anchor='ne')

        # Redirect standard output to this text area
        sys.stdout = TextRedirector(self.text)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        # Get the current position of the scrollbar's view
        current_position = self.widget.yview()
        # Insert new text
        self.widget.insert(tk.END, string)
        # If the scrollbar is at the bottom, auto-scroll to the bottom; otherwise, do not scroll
        if current_position == (0.0, 1.0):
            self.widget.see(tk.END)

    def flush(self):
        pass  # This is to comply with Python's standard output stream

if __name__ == "__main__":
    root = tk.Tk()
    app = TransparentLogWindow(root)
    
    # Test output
    print("This is a test message for the Transparent Log Window.")
    print("You can adjust styles and see the changes live.")

    root.mainloop()