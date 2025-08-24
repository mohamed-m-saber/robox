import tkinter as tk
from tkinter import font, ttk,messagebox
import backend 
from backend import DeviceDetector,process_log_queue
import queue
import time

# Add this to your existing GUI code - integrate camera feed into top_area

import cv2
from PIL import Image, ImageTk
import threading
import queue
import numpy as np



import os
os.environ['ROS_DOMAIN_ID'] = '12'  # Ensure domain ID 12

import tkinter as tk
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from PIL import Image as PILImage, ImageTk

class CameraManager(Node):
    def __init__(self, parent_frame, log_text, log_queue):
        rclpy.init(args=None)
        super().__init__('camera_manager_gui_node')

        self.parent_frame = parent_frame
        self.log_text = log_text
        self.log_queue = log_queue

        self.bridge = CvBridge()
        self.camera_label = None

        self.setup_camera_display()

        self.subscription = self.create_subscription(
            Image, 'detection_feed', self.image_callback, 10)
        self.get_logger().info("🖥️ Subscribed to detection_feed")
        self.log_message("Detection feed started")

    def setup_camera_display(self):
        camera_frame = tk.Frame(self.parent_frame, bg="#EEEDED", relief="solid", bd=1)
        camera_frame.pack(fill='both', expand=True, padx=10, pady=10)

        title_label = tk.Label(camera_frame, text="Detection Feed",
                               font=("Helvetica", 14, "bold"),
                               bg="#EEEDED", fg="#404680")
        title_label.pack(pady=(10, 5))

        self.camera_label = tk.Label(camera_frame, text="Waiting for feed...",
                                     bg="#EEEDED", fg="#666666",
                                     font=("Helvetica", 12))
        self.camera_label.pack(expand=True)

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Resize frame to desired dimensions
            target_width = 840
            target_height = 660
            resized_frame = cv2.resize(cv_image, (target_width, target_height))

            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            pil_image = PILImage.fromarray(rgb_frame)
            photo = ImageTk.PhotoImage(pil_image)

            self.camera_label.configure(image=photo, text="")
            self.camera_label.image = photo

        except Exception as e:
            self.log_message(f"Feed error: {str(e)}")


    def log_message(self, message):
        self.log_queue.put(f"[Feed] {message}")
    def shutdown(self):
        self.get_logger().info("Shutting down camera manager GUI node.")
        # if self.subscription:
        #     self.destroy_subscription(self.subscription)
        self.camera_label.configure(image="", text="Waiting for feed...")
        self.camera_label.image = None
        


# Modify your create_main_window function to include camera manager
def create_main_window():
    root = tk.Tk()
    root.geometry("1000x980")
    root.title("Robox Robotics AI Kit")
    root.configure(bg="#F8F9FA")

    setup_styles()

    # Create log queue for thread-safe logging
    log_queue = queue.Queue()

    # Create main layout
    sidebar = ttk.Frame(root, style="Sidebar.TFrame", width=300)
    sidebar.pack(side='left', fill='y')
    sidebar.pack_propagate(False)

    # Main area
    main_area = ttk.Frame(root, style="Main.TFrame")
    main_area.pack(side='right', fill='both', expand=True)

    # Split main_area into top and bottom frames using pack
    top_area = ttk.Frame(main_area, style="Main.TFrame")
    top_area.pack(side='top', fill='both', expand=True)

    log_area = ttk.Frame(main_area, style="Main.TFrame")
    log_area.pack(side='bottom', fill='x')

    # CREATE CAMERA MANAGER HERE
    # In your main app
    frame_queue = queue.Queue(maxsize=2)

    # color_pose_client = ColorPoseClient(frame_queue=frame_queue, show_window=False)

    # Label for log area
    log_label = ttk.Label(log_area, text="Real-time Output", style="Mode.TLabelframe.Label")
    log_label.pack(anchor="w", padx=8, pady=(4, 0))

    # Text widget for logs with scrollbar
    log_frame = tk.Frame(log_area, bg="#F0F0F0")
    log_frame.pack(fill='x', padx=8, pady=6)

    log_text = tk.Text(log_frame, height=12, bg="#F0F0F0", relief="solid", bd=1, wrap=tk.WORD)
    scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=log_text.yview)
    log_text.configure(yscrollcommand=scrollbar.set)
    
    log_text.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar.pack(side=tk.RIGHT, fill='y')
    camera_manager = CameraManager(top_area, log_text, log_queue)
    
    def run_ros_spin():
        while rclpy.ok():
            rclpy.spin_once(camera_manager, timeout_sec=0.05)

    threading.Thread(target=run_ros_spin, daemon=True).start()



    # Sidebar header
    header_frame = tk.Frame(sidebar, bg="#404680", height=60)
    header_frame.pack(fill='x', pady=0)
    header_frame.pack_propagate(False)

    title_label = tk.Label(header_frame, text="Robox Control", 
                        font=("Helvetica", 16, "bold"), 
                        bg="#404680", fg="#ECF0F1")
    title_label.pack(pady=15)

    create_sidebar_sections(sidebar, log_text, log_queue,camera_manager)

    # Add welcome message to log
    log_text.insert(tk.END, "Welcome to Robox Robotics AI Kit Control Panel\n")
    log_text.insert(tk.END, "Select a mode and click Execute to begin\n")
    log_text.insert(tk.END, "Real-time launch file output will appear below\n")
    log_text.insert(tk.END, "Device detection is running in background...\n")
    log_text.insert(tk.END, "=" * 50 + "\n")

    # Start the log queue processor
    root.after(100, process_log_queue, log_text, log_queue, root)
    
    # Handle window closing
    def on_closing():
        rclpy.shutdown()
        camera_manager.shutdown()
        root.quit()
        root.destroy()

    
        

    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    return root

class DeviceLED(tk.Canvas):
    def __init__(self, parent, device_name, width=20, height=20):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        
        self.device_name = device_name
        self.width = width
        self.height = height
        self.is_connected = False
        self.blink_state = False
        self.blink_job = None
        
        # Configure background to match parent
        self.configure(bg=parent.cget('bg'))
        
        self.draw_led()
        
    def draw_led(self):
        self.delete("all")
        
        # Draw LED circle
        radius = min(self.width, self.height) // 2 - 2
        center_x = self.width // 2
        center_y = self.height // 2
        
        if self.is_connected:
            # Solid green for connected
            color = "#27AE60"
            self.create_oval(center_x - radius, center_y - radius,
                           center_x + radius, center_y + radius,
                           fill=color, outline="#1E8449", width=2)
        else:
            # Blinking red for disconnected
            color = "#E74C3C" if self.blink_state else "#C0392B"
            self.create_oval(center_x - radius, center_y - radius,
                           center_x + radius, center_y + radius,
                           fill=color, outline="#A93226", width=2)
    
    def set_connected(self, connected):
        self.is_connected = connected
        
        if connected:
            # Stop blinking and show solid green
            if self.blink_job:
                self.after_cancel(self.blink_job)
                self.blink_job = None
            self.draw_led()
        else:
            # Start blinking red
            if not self.blink_job:
                self.start_blinking()
    
    def start_blinking(self):
        self.blink_state = not self.blink_state
        self.draw_led()
        self.blink_job = self.after(500, self.start_blinking)  # Blink every 500ms




class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color="#4A90E2", hover_color="#357ABD", 
                 text_color="white", width=200, height=45, corner_radius=15):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        
        self.command = command
        self.original_bg_color = bg_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        self.text = text
        self.enabled = True
        self.last_click_time = 0  # Track last click time for cooldown

        self.configure(bg=parent.cget('bg'))
        self.draw_button()

        # Bind mouse events
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self):
        self.delete("all")
        color = self.bg_color if self.enabled else "#CCCCCC"

        # Draw rounded rectangle background
        self.create_rounded_rectangle(2, 2, self.width-2, self.height-2, 
                                      self.corner_radius, fill=color, outline="")

        # Draw button text
        text_color = self.text_color if self.enabled else "#666666"
        self.create_text(self.width // 2, self.height // 2, text=self.text, 
                         fill=text_color, font=("Helvetica", 11, "bold"))

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        if self.enabled and self.command:
            current_time = time.time()
            if current_time - self.last_click_time >= 5:
                # Record time and run command
                self.last_click_time = current_time
                self.command()

                # Disable button and re-enable after 5 seconds
                self.set_enabled(False)
                self.after(5000, lambda: self.set_enabled(True))
            else:
                # Show messagebox if clicked too fast
                messagebox.showinfo("Cooldown", "Please wait 5 seconds before clicking again.")

    def on_enter(self, event):
        if self.enabled:
            self.bg_color = self.hover_color
            self.draw_button()

    def on_leave(self, event):
        if self.enabled:
            self.bg_color = self.original_bg_color
            self.draw_button()

    def set_enabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self.bg_color = self.original_bg_color
        else:
            self.bg_color = "#CCCCCC"
        self.draw_button()


def setup_styles():
    """Configure ttk styles for the application"""
    style = ttk.Style()
    style.theme_use("clam")

    # Sidebar styling
    style.configure("Sidebar.TFrame", background="#404680")
    style.configure("Main.TFrame", background="#EEEDED")

    # Mode frame styling
    style.configure("Mode.TLabelframe", 
                   background="#EEEDED", 
                   borderwidth=1, 
                   relief="flat")
    style.configure("Mode.TLabelframe.Label", 
                   font=("Helvetica", 16, "bold"),
                   foreground="#404680",
                   background="#EEEDED",
                   padding=(20,8,20,4))

    # Regular labels
    style.configure("TLabel", 
                   background="#EEEDED", 
                   foreground="#34495E", 
                   font=("Helvetica", 10))
    
    style.configure("Sidebar.TLabel", 
                   background="#404680", 
                   foreground="#EEEDED", 
                   font=("Helvetica", 18, "bold"))

    # Combobox styling
    style.configure("TCombobox", 
                   fieldbackground="#EEEDED", 
                   background="#EEEDED",
                   borderwidth=5,
                   relief="flat")
    style.map("TCombobox", 
              fieldbackground=[("readonly", "#EEEDED")],
              selectbackground=[("readonly", "#3498DB")])

    # Checkbuttons
    style.configure("TCheckbutton", 
                   background="#EEEDED", 
                   foreground="#34495E",
                   font=("Helvetica", 10),
                   focuscolor="none")
    style.map("TCheckbutton",
              background=[("active", "#EEEDED"), ("selected", "#EEEDED")],
              foreground=[("active", "#2980B9")])




def create_device_status_panel(parent, log_text, log_queue):
    """Create device status panel with LEDs"""
    status_frame = tk.Frame(parent, bg="#404680")
    status_frame.pack(fill='x', pady=4, padx=15)
    
    # Title
    status_title = tk.Label(status_frame, text="Device Status", 
                           font=("Helvetica", 12, "bold"), 
                           bg="#404680", fg="#ECF0F1")
    status_title.pack(pady=(0, 8))
    
    # Arduino status
    arduino_frame = tk.Frame(status_frame, bg="#404680")
    arduino_frame.pack(fill='x', pady=2)
    arduino_led = DeviceLED(arduino_frame, "Arduino")
    arduino_led.pack(side='left', padx=(0, 8))
    arduino_label = tk.Label(arduino_frame, text="Arduino", font=("Helvetica", 10), bg="#404680", fg="#ECF0F1")
    arduino_label.pack(side='left')

    # Camera status
    # camera_frame = tk.Frame(status_frame, bg="#404680")
    # camera_frame.pack(fill='x', pady=2)
    # camera_led = DeviceLED(camera_frame, "Camera")
    # camera_led.pack(side='left', padx=(0, 8))
    # camera_label = tk.Label(camera_frame, text="Camera", font=("Helvetica", 10), bg="#404680", fg="#ECF0F1")
    # camera_label.pack(side='left')

    # Joystick status
    joystick_frame = tk.Frame(status_frame, bg="#404680")
    joystick_frame.pack(fill='x', pady=2)
    joystick_led = DeviceLED(joystick_frame, "Joystick")
    joystick_led.pack(side='left', padx=(0, 8))
    joystick_label = tk.Label(joystick_frame, text="Joystick", font=("Helvetica", 10), bg="#404680", fg="#ECF0F1")
    joystick_label.pack(side='left')
    
    # Create and start device detector
    detector = DeviceDetector(arduino_led, joystick_led, log_text, log_queue)
    detector.start_detection()

    return detector



def build_color_stacking_widgets(parent):
    stacking_frame = ttk.Frame(parent, style="TFrame")
    stacking_frame.pack(pady=5, fill='x', padx=5)

    stacking_combos = {}
    priority_options = ["1", "2", "3"]
    colors = ["Red   ", "Green", "Blue  "]
    color_codes = {"Red   ": "#E74C3C", "Green": "#27AE60", "Blue  ": "#3498DB"}

    for i, color in enumerate(colors):
        row = ttk.Frame(stacking_frame, style="TFrame")
        row.pack(anchor="w", pady=2, fill='x')

        # Color indicator
        color_indicator = tk.Frame(row, bg=color_codes[color], width=15, height=15)
        color_indicator.pack(side="left", padx=(0, 8))

        label = ttk.Label(row, text=f"{color}:", style="TLabel")
        label.pack(side="left", padx=3)
        
        combo = ttk.Combobox(row, values=priority_options, width=6, state="readonly")
        combo.pack(side="left", padx=3)
        stacking_combos[color] = combo

    return stacking_combos


def build_color_tracking_widgets(parent, tracking_subwidgets):
    # Configure styles for TCheckbutton and TFrame
    style = ttk.Style()
    style.configure("TCheckbutton", background="#EEEDED")
    style.configure("TFrame", background="#EEEDED")

    tracking_frame = ttk.Frame(parent, style="TFrame")
    tracking_frame.pack(pady=5, fill='x', padx=5)

    colors = ["Red   ", "Green", "Blue  "]
    color_codes = {"Red   ": "#E74C3C", "Green": "#27AE60", "Blue  ": "#3498DB"}

    # Variable to track which color is selected
    selected_color = tk.StringVar()

    for color in colors:
        row = ttk.Frame(tracking_frame, style="TFrame")
        row.pack(anchor="w", pady=2, fill='x')

        # Color indicator
        color_indicator = tk.Frame(row, bg=color_codes[color], width=15, height=15)
        color_indicator.pack(side="left", padx=(0, 8))

        # Use radiobutton for single selection
        btn = ttk.Radiobutton(row, text=color, variable=selected_color, 
                             value=color, style="TCheckbutton")
        btn.pack(side="left", padx=3)
        tracking_subwidgets[color] = btn

    return tracking_frame

def execute_btn(mode_frame, mode, execute_buttons, stacking_combos, process_handles, tracking_subwidgets, log_text, log_queue):
    """Create execute button for a mode"""
    button_frame = tk.Frame(mode_frame, bg="#EEEDED")
    button_frame.pack(pady=5, fill='x')

    execute_btn = RoundedButton(
        button_frame, 
        text="Execute",
        command=lambda m=mode: backend.activate_b(
            m, process_handles, stacking_combos, tracking_subwidgets, execute_buttons, log_text, log_queue),
        bg_color="#4A90E2",
        hover_color="#357ABD",
        width=150,
        height=35
    )
    execute_btn.pack(pady=3)

    execute_buttons[mode] = execute_btn


def quit_btn(sidebar, process_handles, execute_buttons, log_text, log_queue, camera_manager):
    """Create quit and clear log buttons"""
    button_container = tk.Frame(sidebar, bg="#404680")
    button_container.pack(pady=15, padx=15, fill='x')

    # Quit button
    quit_btn = RoundedButton(
        button_container,
        text="Quit",
        command=lambda: [backend.quit_b(process_handles, log_text), backend.quit_f(execute_buttons),camera_manager.shutdown()
],
        bg_color="#E74C3C",
        hover_color="#C0392B",
        width=250,
        height=40
    )
    quit_btn.pack(pady=5)

    # Clear log button
    clear_btn = RoundedButton(
        button_container,
        text="Clear Log",
        command=lambda: backend.clear_log(log_text),
        bg_color="#F39C12",
        hover_color="#E67E22",
        width=250,
        height=35
    )
    clear_btn.pack(pady=5)



def create_sidebar_sections(sidebar, log_text, log_queue,camera_manager):
    # Create mode sections
    stacking_combos = {}
    tracking_subwidgets = {}
    process_handles = {}
    execute_buttons = {}

    # Add device status panel first
    device_detector = create_device_status_panel(sidebar, log_text, log_queue)

    modes = ["\n  Color Sorting", "\n  Color Stacking", "\n  Color Tracking", "\n  QR Detection", "\n  Joystick"]
    for mode in modes:
        mode_container = tk.Frame(sidebar, bg="#404680")
        mode_container.pack(pady=1, padx=12, fill='x')

        mode_frame = ttk.LabelFrame(mode_container, 
                                    text=mode, 
                                    style="Mode.TLabelframe",
                                    padding=1)
        mode_frame.pack(fill='x')

        # Mode-specific widgets
        if mode == "\n  Color Stacking":
            stacking_combos.update(build_color_stacking_widgets(mode_frame))
        elif mode == "\n  Color Tracking":
            build_color_tracking_widgets(mode_frame, tracking_subwidgets)

        execute_btn(mode_frame, mode.strip(), execute_buttons, stacking_combos, process_handles, tracking_subwidgets, log_text, log_queue)

    quit_btn(sidebar, process_handles, execute_buttons, log_text, log_queue,camera_manager)

"#EEEDED"




