import tkinter as tk
from tkinter import filedialog
import cv2
import torch
from terminal import Terminal  # Import the Terminal class from terminal.py
from clock import Clock  # Import the Clock class from clock.py
from codeline import code_lines  # Import the code lines from codeline.py
import subprocess

# Load the pre-trained YOLOv5 model

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

class HumanDetectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Human Detection")

        # Set the window to full screen and disable the option to exit full screen
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.exit_fullscreen)

        self.master.configure(bg="black")

        # Initialize the clock in the top-right corner
        self.clock = Clock(master)

        # Create a terminal
        self.terminal = Terminal(master)
        self.terminal.place(relx=0.65, rely=0.53, anchor=tk.CENTER, width=1000, height=690)  # Position terminal at the right side

        # Start typing the code in the terminal
        self.master.after(100, lambda: self.terminal.type_code(code_lines))  # Call type_code after a short delay

        self.label = tk.Label(master, text="OBJECT DETECTOR", fg="cyan", bg="black", font=("Recharge Rg", 23, "bold"))
        self.label.place(relx=0.5, rely=0.07, anchor=tk.CENTER)  # Center the label on the left side
        
        # Create buttons and label with modified fonts and styles
        self.label = tk.Label(master, text="Choose an option:", fg="cyan", bg="black", font=("Recharge Rg", 16, "bold"))
        self.label.place(relx=0.2, rely=0.15, anchor=tk.CENTER)  # Center the label on the left side

        # Set width and height for all buttons to make them equal
        button_width = 20
        button_height = 2

        # Position buttons more to the left side of the screen
        self.btn_camera = tk.Button(master, text="Launch Camera", command=self.launch_camera, font=("Helvetica", 16, "bold"), 
        bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_camera.place(relx=0.2, rely=0.23, anchor=tk.CENTER)

        self.btn_droidcam = tk.Button(master, text="Connect to MyPhone", command=self.connect_droidcam, font=("Helvetica", 16, "bold"), 
        bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_droidcam.place(relx=0.2, rely=0.33, anchor=tk.CENTER)

        self.btn_video = tk.Button(master, text="Select Video", command=self.select_video, font=("Helvetica", 16, "bold"), 
        bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_video.place(relx=0.2, rely=0.43, anchor=tk.CENTER)

        self.btn_image = tk.Button(master, text="Select Image", command=self.select_image, font=("Helvetica", 16, "bold"), 
        bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_image.place(relx=0.2, rely=0.53, anchor=tk.CENTER)

        # New button for PowerPoint
        self.btn_ppt = tk.Button(master, text="Show PowerPoint", command=self.show_ppt, font=("Helvetica", 16, "bold"), 
        bg="cyan", fg="black", width=button_width, height=button_height)
        self.btn_ppt.place(relx=0.2, rely=0.63, anchor=tk.CENTER)

        self.video_source = None

    def launch_camera(self):
        self.video_source = 0  # Default webcam
        self.start_detection()

    def connect_droidcam(self):
        self.video_source = 1  # Connect to DroidCam as a webcam
        self.start_detection()

    def select_video(self):
        self.video_source = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if self.video_source:
            self.start_detection()

    def select_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            self.detect_image(image_path)

    def show_ppt(self):
    # Path to your PowerPoint file in the main directory
        ppt_path = "myppt.pptx"  # Change this to your actual file name

    # Open the PowerPoint presentation
        try:
            # Use subprocess to start PowerPoint
            subprocess.Popen([r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE', ppt_path])

        except Exception as e:
            print(f"Error opening PowerPoint: {e}")

    def start_detection(self):
        cap = cv2.VideoCapture(self.video_source)
        cv2.namedWindow("Human Detection", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Human Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)
            results.render()
            count = (results.pandas().xyxy[0]['name'] == 'person').sum()
            cv2.putText(frame, f'Count: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Human Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def detect_image(self, image_path):
        frame = cv2.imread(image_path)
        results = model(frame)
        results.render()
        count = (results.pandas().xyxy[0]['name'] == 'person').sum()
        cv2.putText(frame, f'Count: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Human Detection', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def exit_fullscreen(self, event=None):
        self.master.attributes('-fullscreen', False)

if __name__ == "__main__":
    root = tk.Tk()
    app = HumanDetectionApp(root)
    root.mainloop()