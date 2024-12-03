import tkinter as tk
from tkinter import filedialog

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open a file dialog to select the PowerPoint file
ppt_path = filedialog.askopenfilename(title='Select a PowerPoint file', filetypes=[('PowerPoint Files', '*.pptx;*.ppt')])

# Print the selected path
print(ppt_path)
