import tkinter as tk
import time
import pygame  # Import pygame
import threading

class Terminal(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="black", fg="cyan", font=("Recharge Rg", 15), wrap="word")
        self.max_lines = 20  # Set the maximum number of visible lines
        pygame.mixer.init()  # Initialize pygame mixer

    def play_sound(self):
        pygame.mixer.music.load('click.mp3')  # Use the correct path for your sound file
        pygame.mixer.music.play()

    def type_code(self, code_lines):
        self.delete(1.0, tk.END)  # Clear the terminal
        lines = code_lines.strip().splitlines()  # Split the code into lines

        for line in lines:
            for char in line:  # Type character by character
                self.insert(tk.END, char)  # Insert each character
                self.update()  # Update the display
                
                # Play typing sound in a separate thread to avoid blocking
                threading.Thread(target=self.play_sound).start()
                
                time.sleep(0.03)  # Adjust typing speed here
            self.insert(tk.END, "\n")  # Add a newline after each line
            self.update()  # Update the display
            time.sleep(0.1)  # Delay before typing the next line

            # Auto-scroll if the number of lines exceeds max_lines
            if int(self.index('end-1c').split('.')[0]) > self.max_lines:
                self.see(tk.END)  # Scroll to the end

        self.see(tk.END)  # Ensure we scroll to the end after all lines are typed
        
    def toggle_typing(self, event=None):
        if self.typing_active:
            self.typing_active = False  # Stop typing
            if self.typing_thread is not None:
                self.typing_thread.join()  # Wait for the typing thread to finish
        else:
            self.typing_active = True  # Start typing
            self.typing_thread = threading.Thread(target=self.typing_process)
            self.typing_thread.start()  # Start typing in a new thread
            
        self.master.bind("<space>", self.toggle_typing)
