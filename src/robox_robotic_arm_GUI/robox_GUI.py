# import tkinter as tk
# from tkinter import font, ttk, messagebox
# import subprocess
# import os
# import signal


# class RoundedButton(tk.Canvas):
#     def __init__(self, parent, text, command, bg_color="#4A90E2", hover_color="#357ABD", 
#                  text_color="white", width=200, height=45, corner_radius=15):
#         super().__init__(parent, width=width, height=height, highlightthickness=0)
        
#         self.command = command
#         self.original_bg_color = bg_color  # Store original color
#         self.bg_color = bg_color
#         self.hover_color = hover_color
#         self.text_color = text_color
#         self.corner_radius = corner_radius
#         self.width = width
#         self.height = height
#         self.text = text
#         self.enabled = True
        
#         # Configure background to match parent
#         self.configure(bg=parent.cget('bg'))
        
#         self.draw_button()
        
#         # Bind events
#         self.bind("<Button-1>", self.on_click)
#         self.bind("<Enter>", self.on_enter)
#         self.bind("<Leave>", self.on_leave)
        
#     def draw_button(self):
#         self.delete("all")
#         color = self.bg_color if self.enabled else "#CCCCCC"
        
#         # Draw rounded rectangle
#         self.create_rounded_rectangle(2, 2, self.width-2, self.height-2, 
#                                     self.corner_radius, fill=color, outline="")
        
#         # Draw text
#         text_color = self.text_color if self.enabled else "#666666"
#         self.create_text(self.width//2, self.height//2, text=self.text, 
#                         fill=text_color, font=("Helvetica", 11, "bold"))
        
#     def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
#         points = []
#         for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
#                      (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
#                      (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
#                      (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
#             points.extend([x, y])
#         return self.create_polygon(points, smooth=True, **kwargs)
        
#     def on_click(self, event):
#         if self.enabled and self.command:
#             self.command()
            
#     def on_enter(self, event):
#         if self.enabled:
#             self.bg_color = self.hover_color
#             self.draw_button()
            
#     def on_leave(self, event):
#         if self.enabled:
#             self.bg_color = self.original_bg_color  # Use original color instead of hardcoded blue
#             self.draw_button()
            
#     def set_enabled(self, enabled):
#         self.enabled = enabled
#         if enabled:
#             self.bg_color = self.original_bg_color  # Use original color
#         else:
#             self.bg_color = "#CCCCCC"
#         self.draw_button()


# def setup_styles():
#     style = ttk.Style()
#     style.theme_use("clam")

#     # Sidebar styling
#     style.configure("Sidebar.TFrame", background="#404680")
#     style.configure("Main.TFrame", background="#EEEDED")


#     # Mode frame styling
#     style.configure("Mode.TLabelframe", 
#                    background="#EEEDED"
# , 
#                    borderwidth=1, 
#                    relief="flat")
#     style.configure("Mode.TLabelframe.Label", 
#                    font=("Helvetica", 16, "bold"),     # Bigger font
#                    foreground="#404680",               # Light text
#                    background="#EEEDED"
# ,               # Distinct dark background
#                    padding=20)                          # Add padding for space

#     # Regular labels
#     style.configure("TLabel", 
#                    background="#EEEDED"
# , 
#                    foreground="#34495E", 
#                    font=("Helvetica", 10))
    
#     style.configure("Sidebar.TLabel", 
#                    background="#404680", 
#                    foreground="#EEEDED"
# , 
#                    font=("Helvetica", 18, "bold"))

#     # Combobox styling
#     style.configure("TCombobox", 
#                    fieldbackground="#EEEDED"
# , 
#                    background="#EEEDED"
# ,
#                    borderwidth=5,
#                    relief="flat")
#     style.map("TCombobox", 
#               fieldbackground=[("readonly", "#EEEDED"
# )],
#               selectbackground=[("readonly", "#3498DB")])

#     # Checkbuttons
#     style.configure("TCheckbutton", 
#                    background="#EEEDED"
# , 
#                    foreground="#34495E",
#                    font=("Helvetica", 10),
#                    focuscolor="none")
#     style.map("TCheckbutton",
#               background=[("active", "#EEEDED"
# ), ("selected", "#EEEDED"
# )],
#               foreground=[("active", "#2980B9")])


# def operate(command,selected_mode, process_handles):
    
#     print(f"🚀 Launching: {command}")


#     proc = subprocess.Popen(
#     ["bash", "-c", command],
#     preexec_fn=os.setsid
# )
#     process_handles[selected_mode] = proc
    
# def activate_b(selected_mode, process_handles,stacking_combos, tracking_subwidgets,execute_buttons):
#     print(f"▶️ Executing {selected_mode}")
#     launch_commands = {
#     "Color Sorting": "source /opt/ros/jazzy/setup.bash && source /home/saber/robox_ws/install/setup.bash && ros2 launch dashboard color_sorting.launch.py",
#     "Color Stacking": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard color_stacking.launch.py",
#     "Color Tracking": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard color_tracking.launch.py",
#     "QR Detection": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard qr.launch.py",
#     "Joystick": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard joystick.launch.py"
# }
#     # Stop existing processes
#     for mode, proc in process_handles.items():
#         if proc.poll() is None:
#             print(f"🛑 Stopping {mode}")
#             os.killpg(os.getpgid(proc.pid), signal.SIGINT)
#     process_handles.clear()

   

#     # Launch command
#     if selected_mode in launch_commands:
#         command = launch_commands[selected_mode]
#         # Validate Stacking mode inputs
#         if selected_mode == "Color Stacking":
#             selected_values = [combo.get() for combo in stacking_combos.values()]
#             if "" in selected_values:
#                 messagebox.showerror("Incomplete", "Please select a priority for each color.")
#                 return
#             if len(set(selected_values)) != len(selected_values):
#                 messagebox.showerror("Duplicate Priority", "Each priority must be unique.")
#                 return
#             final_priorities = {color: stacking_combos[color].get() for color in stacking_combos}
#             print("✔️ Stacking Priorities:", final_priorities)
#             messagebox.showinfo("Executed", f"Stacking Mode started with priorities: {final_priorities}")
#             operate(command,selected_mode, process_handles)
#             activate_f(selected_mode,execute_buttons)

#         elif selected_mode == "Color Tracking":
#             for color, btn in tracking_subwidgets.items():
#                 if btn.instate(["selected"]):
#                     print(f"Tracking color: {color}")
#                     operate(command,selected_mode, process_handles) 
#                     activate_f(selected_mode,execute_buttons)
 
#                 else:
#                     messagebox.showerror("Error","Please select a color to track")
#                     return
#         else:        
#             operate(command,selected_mode, process_handles)  
#             activate_f(selected_mode,execute_buttons)
        


# def activate_f(selected_mode,execute_buttons):
       
#     # Update button states
#     for mode, btn in execute_buttons.items():
#         if mode == selected_mode:
#             # Change to running state
#             btn.text = "Running"
#             btn.original_bg_color = "#27AE60"  # Green
#             btn.bg_color = "#27AE60"
#             btn.hover_color = "#229954"  # Darker green
#             btn.set_enabled(True)
#         else:
#             btn.set_enabled(False)
#         btn.draw_button()     

           


# def quit_b(process_handles):
#     print("▶️ Quitting all modes")

#     for mode, proc in process_handles.items():
#         if proc.poll() is None:
#             print(f"🛑 Stopping {mode}")
#             os.killpg(os.getpgid(proc.pid), signal.SIGINT)
#     process_handles.clear()

    

# def quit_f(execute_buttons):
#     # Re-enable all execute buttons and restore original state
#     for btn in execute_buttons.values():
#         btn.text = "Execute"
#         btn.original_bg_color = "#4A90E2"  # Blue
#         btn.bg_color = "#4A90E2"
#         btn.hover_color = "#357ABD"  # Darker blue
#         btn.set_enabled(True)
#         btn.draw_button()



# def quit_btn(sidebar,process_handles,execute_buttons):
#      # Quit button
#     quit_container = tk.Frame(sidebar, bg="#404680")
#     quit_container.pack(pady=15, padx=15, fill='x')

#     quit_btn = RoundedButton(
#         quit_container,
#         text="Quit",
#         command=lambda: [quit_b(process_handles),quit_f( execute_buttons)],
#         bg_color="#E74C3C",
#         hover_color="#C0392B",
#         width=250,
#         height=40
#     )
#     quit_btn.pack(pady=5)



# def execute_btn(mode_frame,mode,execute_buttons,stacking_combos,process_handles,tracking_subwidgets):
#      # Execute button
#         button_frame = tk.Frame(mode_frame, bg="#EEEDED")
#         button_frame.pack(pady=5, fill='x')

#         execute_btn = RoundedButton(
#             button_frame, 
#             text="Execute",
#             command=lambda m=mode:activate_b(
#                 m,  process_handles,stacking_combos, tracking_subwidgets,execute_buttons) ,
#             bg_color="#4A90E2",
#             hover_color="#357ABD",
#             width=150,
#             height=35
#         )
#         execute_btn.pack(pady=3)

#         execute_buttons[mode] = execute_btn    
     
# def build_color_stacking_widgets(parent):
#     stacking_frame = ttk.Frame(parent, style="TFrame")
#     stacking_frame.pack(pady=5, fill='x', padx=5)

#     stacking_combos = {}
#     priority_options = ["1", "2", "3"]
#     colors = ["Red", "Green", "Blue"]
#     color_codes = {"Red": "#E74C3C", "Green": "#27AE60", "Blue": "#3498DB"}

#     for i, color in enumerate(colors):
#         row = ttk.Frame(stacking_frame, style="TFrame")
#         row.pack(anchor="w", pady=2, fill='x')

#         # Color indicator
#         color_indicator = tk.Frame(row, bg=color_codes[color], width=15, height=15)
#         color_indicator.pack(side="left", padx=(0, 8))

#         label = ttk.Label(row, text=f"{color}:", style="TLabel")
#         label.pack(side="left", padx=3)
        
#         combo = ttk.Combobox(row, values=priority_options, width=6, state="readonly")
#         combo.pack(side="left", padx=3)
#         stacking_combos[color] = combo

#     return stacking_combos

# def build_color_tracking_widgets(parent, tracking_subwidgets):
#     # Configure styles for TCheckbutton and TFrame
#     style = ttk.Style()
#     style.configure("TCheckbutton", background="#EEEDED"
# )  # Radiobutton background
#     style.configure("TFrame", background="#EEEDED"
# )       # Frame background to match

#     tracking_frame = ttk.Frame(parent, style="TFrame")
#     tracking_frame.pack(pady=5, fill='x', padx=5)

#     colors = ["Red", "Green", "Blue"]
#     color_codes = {"Red": "#E74C3C", "Green": "#27AE60", "Blue": "#3498DB"}

#     # Variable to track which color is selected
#     selected_color = tk.StringVar()

#     for color in colors:
#         row = ttk.Frame(tracking_frame, style="TFrame")
#         row.pack(anchor="w", pady=2, fill='x')

#         # Color indicator
#         color_indicator = tk.Frame(row, bg=color_codes[color], width=15, height=15)
#         color_indicator.pack(side="left", padx=(0, 8))

#         # Use radiobutton for single selection
#         btn = ttk.Radiobutton(row, text=color, variable=selected_color, 
#                              value=color, style="TCheckbutton")
#         btn.pack(side="left", padx=3)
#         tracking_subwidgets[color] = btn

#     return tracking_frame

# def create_sidebar_sections(sidebar):
#     # Create mode sections
#     stacking_combos = {}
#     tracking_subwidgets = {}
#     process_handles = {}
#     execute_buttons = {}

#     modes = ["Color Sorting", "Color Stacking", "Color Tracking", "QR Detection", "Joystick"]
#     for mode in modes:
#         style = ttk.Style()
#         style.configure("Mode.TLabelframe", 
#                         labelmargins=[6, 6, 6, 6],
#                         background="#EEEDED",
#                         foreground="#EEEDED")

#         mode_container = tk.Frame(sidebar, bg="#404680")
#         mode_container.pack(pady=6, padx=12, fill='x')

#         mode_frame = ttk.LabelFrame(mode_container, 
#                                     text=mode, 
#                                     style="Mode.TLabelframe",
#                                     padding=6)
#         mode_frame.pack(fill='x')

#         # Mode-specific widgets
#         if mode == "Color Stacking":
#             stacking_combos.update(build_color_stacking_widgets(mode_frame))
#         elif mode == "Color Tracking":
#             build_color_tracking_widgets(mode_frame, tracking_subwidgets)

#         # execute_buttons[mode] = execute_btn
#         execute_btn(mode_frame,mode,execute_buttons,stacking_combos,process_handles,tracking_subwidgets)


#     quit_btn(sidebar,process_handles,execute_buttons)    
    


# def main():

    


#     root = tk.Tk()
#     root.geometry("1200x900")
#     root.title("Robox Robotics AI Kit")
#     root.configure(bg="#F8F9FA")

#     setup_styles()

#     # Create main layout
#     sidebar = ttk.Frame(root, style="Sidebar.TFrame", width=300)
#     sidebar.pack(side='left', fill='y')
#     sidebar.pack_propagate(False)     #“Don’t shrink or grow your size based on the widgets you pack inside. Stay at the fixed width and height you were given.”

#    # Main area
#     main_area = ttk.Frame(root, style="Main.TFrame")
#     main_area.pack(side='right', fill='both', expand=True)

#     # Split main_area into top and bottom frames using pack
#     top_area = ttk.Frame(main_area, style="Main.TFrame")
#     top_area.pack(side='top', fill='both', expand=True)

#     log_area = ttk.Frame(main_area, style="Main.TFrame")
#     log_area.pack(side='bottom', fill='x')

#     # Label for log area
#     log_label = ttk.Label(log_area, text="Output", style="Mode.TLabelframe.Label")
#     log_label.pack(anchor="w", padx=8, pady=(4, 0))

#     # Text widget for logs
#     log_text = tk.Text(log_area, height=12, bg="#F0F0F0", relief="solid", bd=1)
#     log_text.pack(fill='x', padx=8, pady=6)


#     # Sidebar header
#     header_frame = tk.Frame(sidebar, bg="#404680", height=60)
#     header_frame.pack(fill='x', pady=0)
#     header_frame.pack_propagate(False)

#     title_label = tk.Label(header_frame, text="Robox Control", 
#                         font=("Helvetica", 16, "bold"), 
#                         bg="#404680", fg="#ECF0F1")
#     title_label.pack(pady=15)


#     create_sidebar_sections(sidebar)

    
#     root.mainloop()


# if __name__ == '__main__':
#     main()







# import tkinter as tk
# from tkinter import font, ttk, messagebox
# import subprocess
# import os
# import signal
# import threading
# import queue


# class RoundedButton(tk.Canvas):
#     def __init__(self, parent, text, command, bg_color="#4A90E2", hover_color="#357ABD", 
#                  text_color="white", width=200, height=45, corner_radius=15):
#         super().__init__(parent, width=width, height=height, highlightthickness=0)
        
#         self.command = command
#         self.original_bg_color = bg_color
#         self.bg_color = bg_color
#         self.hover_color = hover_color
#         self.text_color = text_color
#         self.corner_radius = corner_radius
#         self.width = width
#         self.height = height
#         self.text = text
#         self.enabled = True
        
#         # Configure background to match parent
#         self.configure(bg=parent.cget('bg'))
        
#         self.draw_button()
        
#         # Bind events
#         self.bind("<Button-1>", self.on_click)
#         self.bind("<Enter>", self.on_enter)
#         self.bind("<Leave>", self.on_leave)
        
#     def draw_button(self):
#         self.delete("all")
#         color = self.bg_color if self.enabled else "#CCCCCC"
        
#         # Draw rounded rectangle
#         self.create_rounded_rectangle(2, 2, self.width-2, self.height-2, 
#                                     self.corner_radius, fill=color, outline="")
        
#         # Draw text
#         text_color = self.text_color if self.enabled else "#666666"
#         self.create_text(self.width//2, self.height//2, text=self.text, 
#                         fill=text_color, font=("Helvetica", 11, "bold"))
        
#     def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
#         points = []
#         for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
#                      (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
#                      (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
#                      (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
#             points.extend([x, y])
#         return self.create_polygon(points, smooth=True, **kwargs)
        
#     def on_click(self, event):
#         if self.enabled and self.command:
#             self.command()
            
#     def on_enter(self, event):
#         if self.enabled:
#             self.bg_color = self.hover_color
#             self.draw_button()
            
#     def on_leave(self, event):
#         if self.enabled:
#             self.bg_color = self.original_bg_color
#             self.draw_button()
            
#     def set_enabled(self, enabled):
#         self.enabled = enabled
#         if enabled:
#             self.bg_color = self.original_bg_color
#         else:
#             self.bg_color = "#CCCCCC"
#         self.draw_button()


# def setup_styles():
#     style = ttk.Style()
#     style.theme_use("clam")

#     # Sidebar styling
#     style.configure("Sidebar.TFrame", background="#404680")
#     style.configure("Main.TFrame", background="#EEEDED")

#     # Mode frame styling
#     style.configure("Mode.TLabelframe", 
#                    background="#EEEDED", 
#                    borderwidth=1, 
#                    relief="flat")
#     style.configure("Mode.TLabelframe.Label", 
#                    font=("Helvetica", 16, "bold"),
#                    foreground="#404680",
#                    background="#EEEDED",
#                    padding=20)

#     # Regular labels
#     style.configure("TLabel", 
#                    background="#EEEDED", 
#                    foreground="#34495E", 
#                    font=("Helvetica", 10))
    
#     style.configure("Sidebar.TLabel", 
#                    background="#404680", 
#                    foreground="#EEEDED", 
#                    font=("Helvetica", 18, "bold"))

#     # Combobox styling
#     style.configure("TCombobox", 
#                    fieldbackground="#EEEDED", 
#                    background="#EEEDED",
#                    borderwidth=5,
#                    relief="flat")
#     style.map("TCombobox", 
#               fieldbackground=[("readonly", "#EEEDED")],
#               selectbackground=[("readonly", "#3498DB")])

#     # Checkbuttons
#     style.configure("TCheckbutton", 
#                    background="#EEEDED", 
#                    foreground="#34495E",
#                    font=("Helvetica", 10),
#                    focuscolor="none")
#     style.map("TCheckbutton",
#               background=[("active", "#EEEDED"), ("selected", "#EEEDED")],
#               foreground=[("active", "#2980B9")])


# def log_output_reader(process, mode_name, log_queue):
#     """Thread function to read process output and put it in queue"""
#     try:
#         while True:
#             output = process.stdout.readline()
#             if output == '' and process.poll() is not None:
#                 break
#             if output:
#                 log_queue.put((mode_name, "stdout", output.strip()))
        
#         # Read any remaining stderr
#         stderr_output = process.stderr.read()
#         if stderr_output:
#             log_queue.put((mode_name, "stderr", stderr_output.strip()))
            
#     except Exception as e:
#         log_queue.put((mode_name, "error", f"Error reading output: {str(e)}"))


# def process_log_queue(log_text, log_queue, root):
#     """Process items from the log queue and update the text widget"""
#     try:
#         while True:
#             mode_name, stream_type, message = log_queue.get_nowait()
            
#             # Add timestamp and format message
#             timestamp = tk.StringVar()
            
#             if stream_type == "stdout":
#                 log_text.insert(tk.END, f"[{mode_name}] {message}\n")
#             elif stream_type == "stderr":
#                 log_text.insert(tk.END, f"[{mode_name}] ERROR: {message}\n")
#             elif stream_type == "error":
#                 log_text.insert(tk.END, f"[{mode_name}] SYSTEM ERROR: {message}\n")
            
#             # Auto-scroll to bottom
#             log_text.see(tk.END)
            
#             # Limit log size (keep last 1000 lines)
#             lines = log_text.get("1.0", tk.END).split('\n')
#             if len(lines) > 1000:
#                 log_text.delete("1.0", f"{len(lines)-1000}.0")
                
#     except queue.Empty:
#         pass
#     except Exception as e:
#         print(f"Error processing log queue: {e}")
    
#     # Schedule next check
#     root.after(100, process_log_queue, log_text, log_queue, root)


# def operate(command, selected_mode, process_handles, log_text, log_queue):
#     print(f"🚀 Launching: {command}")
#     log_text.insert(tk.END, f"🚀 Launching: {selected_mode}\n")
#     log_text.see(tk.END)
    
#     try:
#         proc = subprocess.Popen(
#             ["bash", "-c", command],
#             preexec_fn=os.setsid,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             bufsize=1,  # Line buffered
#             universal_newlines=True
#         )
#         process_handles[selected_mode] = proc
        
#         # Start thread to read output
#         output_thread = threading.Thread(
#             target=log_output_reader, 
#             args=(proc, selected_mode, log_queue),
#             daemon=True
#         )
#         output_thread.start()
        
#         log_text.insert(tk.END, f"✅ {selected_mode} started successfully\n")
#         log_text.insert(tk.END, f"📋 Logging output from {selected_mode}...\n")
        
#     except Exception as e:
#         log_text.insert(tk.END, f"❌ Error starting {selected_mode}: {str(e)}\n")
#     log_text.see(tk.END)

    
# def activate_b(selected_mode, process_handles, stacking_combos, tracking_subwidgets, execute_buttons, log_text, log_queue):
#     print(f"▶️ Executing {selected_mode}")
#     log_text.insert(tk.END, f"▶️ Executing {selected_mode}\n")
#     log_text.see(tk.END)
    
#     launch_commands = {
#         "Color Sorting": "source /opt/ros/jazzy/setup.bash && source /home/saber/robox_ws/install/setup.bash && ros2 launch dashboard color_sorting.launch.py",
#         "Color Stacking": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard color_stacking.launch.py",
#         "Color Tracking": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard color_tracking.launch.py",
#         "QR Detection": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard qr.launch.py",
#         "Joystick": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard joystick.launch.py"
#     }
    
#     # Stop existing processes
#     for mode, proc in process_handles.items():
#         if proc.poll() is None:
#             print(f"🛑 Stopping {mode}")
#             log_text.insert(tk.END, f"🛑 Stopping {mode}\n")
#             log_text.see(tk.END)
#             os.killpg(os.getpgid(proc.pid), signal.SIGINT)
#     process_handles.clear()

#     # Launch command
#     if selected_mode in launch_commands:
#         command = launch_commands[selected_mode]
        
#         # Validate Stacking mode inputs
#         if selected_mode == "Color Stacking":
#             selected_values = [combo.get() for combo in stacking_combos.values()]
#             if "" in selected_values:
#                 messagebox.showerror("Incomplete", "Please select a priority for each color.")
#                 return
#             if len(set(selected_values)) != len(selected_values):
#                 messagebox.showerror("Duplicate Priority", "Each priority must be unique.")
#                 return
#             final_priorities = {color: stacking_combos[color].get() for color in stacking_combos}
#             print("✔️ Stacking Priorities:", final_priorities)
#             log_text.insert(tk.END, f"✔️ Stacking Priorities: {final_priorities}\n")
#             log_text.see(tk.END)
#             messagebox.showinfo("Executed", f"Stacking Mode started with priorities: {final_priorities}")
#             operate(command, selected_mode, process_handles, log_text, log_queue)
#             activate_f(selected_mode, execute_buttons)

#         elif selected_mode == "Color Tracking":
#             selected_color = None
#             for color, btn in tracking_subwidgets.items():
#                 if btn.instate(["selected"]):
#                     selected_color = color
#                     print(f"Tracking color: {color}")
#                     log_text.insert(tk.END, f"Tracking color: {color}\n")
#                     log_text.see(tk.END)
#                     break
            
#             if selected_color:
#                 send_tracking_param(selected_color, log_text)
  
#                 operate(command, selected_mode, process_handles, log_text, log_queue)
#                 activate_f(selected_mode, execute_buttons)
#             else:
#                 messagebox.showerror("Error", "Please select a color to track")
#                 return
#         else:        
#             operate(command, selected_mode, process_handles, log_text, log_queue)
#             activate_f(selected_mode, execute_buttons)


# def activate_f(selected_mode, execute_buttons):
#     # Update button states
#     for mode, btn in execute_buttons.items():
#         if mode == selected_mode:
#             # Change to running state
#             btn.text = "Running"
#             btn.original_bg_color = "#27AE60"  # Green
#             btn.bg_color = "#27AE60"
#             btn.hover_color = "#229954"  # Darker green
#             btn.set_enabled(True)
#         else:
#             btn.set_enabled(False)
#         btn.draw_button()


# def quit_b(process_handles, log_text):
#     print("▶️ Quitting all modes")
#     log_text.insert(tk.END, "▶️ Quitting all modes\n")
#     log_text.see(tk.END)

#     for mode, proc in process_handles.items():
#         if proc.poll() is None:
#             print(f"🛑 Stopping {mode}")
#             log_text.insert(tk.END, f"🛑 Stopping {mode}\n")
#             log_text.see(tk.END)
#             os.killpg(os.getpgid(proc.pid), signal.SIGINT)
#     process_handles.clear()
#     log_text.insert(tk.END, "✅ All processes stopped\n")
#     log_text.see(tk.END)


# def quit_f(execute_buttons):
#     # Re-enable all execute buttons and restore original state
#     for btn in execute_buttons.values():
#         btn.text = "Execute"
#         btn.original_bg_color = "#4A90E2"  # Blue
#         btn.bg_color = "#4A90E2"
#         btn.hover_color = "#357ABD"  # Darker blue
#         btn.set_enabled(True)
#         btn.draw_button()


# def clear_log(log_text):
#     """Clear the log text widget"""
#     log_text.delete("1.0", tk.END)
#     log_text.insert(tk.END, "Log cleared\n")
#     log_text.insert(tk.END, "=" * 50 + "\n")


# def quit_btn(sidebar, process_handles, execute_buttons, log_text, log_queue):
#     # Button container
#     button_container = tk.Frame(sidebar, bg="#404680")
#     button_container.pack(pady=15, padx=15, fill='x')

#     # Quit button
#     quit_btn = RoundedButton(
#         button_container,
#         text="Quit",
#         command=lambda: [quit_b(process_handles, log_text), quit_f(execute_buttons)],
#         bg_color="#E74C3C",
#         hover_color="#C0392B",
#         width=250,
#         height=40
#     )
#     quit_btn.pack(pady=5)

#     # Clear log button
#     clear_btn = RoundedButton(
#         button_container,
#         text="Clear Log",
#         command=lambda: clear_log(log_text),
#         bg_color="#F39C12",
#         hover_color="#E67E22",
#         width=250,
#         height=35
#     )
#     clear_btn.pack(pady=5)


# def execute_btn(mode_frame, mode, execute_buttons, stacking_combos, process_handles, tracking_subwidgets, log_text, log_queue):
#     # Execute button
#     button_frame = tk.Frame(mode_frame, bg="#EEEDED")
#     button_frame.pack(pady=5, fill='x')

#     execute_btn = RoundedButton(
#         button_frame, 
#         text="Execute",
#         command=lambda m=mode: activate_b(
#             m, process_handles, stacking_combos, tracking_subwidgets, execute_buttons, log_text, log_queue),
#         bg_color="#4A90E2",
#         hover_color="#357ABD",
#         width=150,
#         height=35
#     )
#     execute_btn.pack(pady=3)

#     execute_buttons[mode] = execute_btn


# def build_color_stacking_widgets(parent):
#     stacking_frame = ttk.Frame(parent, style="TFrame")
#     stacking_frame.pack(pady=5, fill='x', padx=5)

#     stacking_combos = {}
#     priority_options = ["1", "2", "3"]
#     colors = ["Red   ", "Green", "Blue  "]
#     color_codes = {"Red   ": "#E74C3C", "Green": "#27AE60", "Blue  ": "#3498DB"}

#     for i, color in enumerate(colors):
#         row = ttk.Frame(stacking_frame, style="TFrame")
#         row.pack(anchor="w", pady=2, fill='x')

#         # Color indicator
#         color_indicator = tk.Frame(row, bg=color_codes[color], width=15, height=15)
#         color_indicator.pack(side="left", padx=(0, 8))

#         label = ttk.Label(row, text=f"{color}:", style="TLabel")
#         label.pack(side="left", padx=3)
        
#         combo = ttk.Combobox(row, values=priority_options, width=6, state="readonly")
#         combo.pack(side="left", padx=3)
#         stacking_combos[color] = combo

#     return stacking_combos


# def build_color_tracking_widgets(parent, tracking_subwidgets):
#     # Configure styles for TCheckbutton and TFrame
#     style = ttk.Style()
#     style.configure("TCheckbutton", background="#EEEDED")
#     style.configure("TFrame", background="#EEEDED")

#     tracking_frame = ttk.Frame(parent, style="TFrame")
#     tracking_frame.pack(pady=5, fill='x', padx=5)

#     colors = ["Red   ", "Green", "Blue  "]
#     color_codes = {"Red   ": "#E74C3C", "Green": "#27AE60", "Blue  ": "#3498DB"}

#     # Variable to track which color is selected
#     selected_color = tk.StringVar()

#     for color in colors:
#         row = ttk.Frame(tracking_frame, style="TFrame")
#         row.pack(anchor="w", pady=2, fill='x')

#         # Color indicator
#         color_indicator = tk.Frame(row, bg=color_codes[color], width=15, height=15)
#         color_indicator.pack(side="left", padx=(0, 8))

#         # Use radiobutton for single selection
#         btn = ttk.Radiobutton(row, text=color, variable=selected_color, 
#                              value=color, style="TCheckbutton")
#         btn.pack(side="left", padx=3)
#         tracking_subwidgets[color] = btn

#     return tracking_frame




# def send_tracking_param(color, log_text):
#     command = f"source /opt/ros/jazzy/setup.bash && ros2 param set /color_pose_publisher target_color \"{color}\""
#     print(f"🔧 Setting param: {command}")
#     log_text.insert(tk.END, f"🔧 Setting target_color = {color}\n")

#     try:
#         result = subprocess.run(
#             ["bash", "-c", command],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         if result.returncode == 0:
#             log_text.insert(tk.END, f"✅ {result.stdout}\n")
#         else:
#             log_text.insert(tk.END, f"❌ {result.stderr}\n")

#     except Exception as e:
#         log_text.insert(tk.END, f"❌ Exception: {str(e)}\n")

#     log_text.see(tk.END)


# def create_sidebar_sections(sidebar, log_text, log_queue):
#     # Create mode sections
#     stacking_combos = {}
#     tracking_subwidgets = {}
#     process_handles = {}
#     execute_buttons = {}

#     modes = ["Color Sorting", "Color Stacking", "Color Tracking", "QR Detection", "Joystick"]
#     for mode in modes:
#         mode_container = tk.Frame(sidebar, bg="#404680")
#         mode_container.pack(pady=6, padx=12, fill='x')

#         mode_frame = ttk.LabelFrame(mode_container, 
#                                     text=mode, 
#                                     style="Mode.TLabelframe",
#                                     padding=6)
#         mode_frame.pack(fill='x')

#         # Mode-specific widgets
#         if mode == "Color Stacking":
#             stacking_combos.update(build_color_stacking_widgets(mode_frame))
#         elif mode == "Color Tracking":
#             build_color_tracking_widgets(mode_frame, tracking_subwidgets)

#         execute_btn(mode_frame, mode, execute_buttons, stacking_combos, process_handles, tracking_subwidgets, log_text, log_queue)

#     quit_btn(sidebar, process_handles, execute_buttons, log_text, log_queue)


# def main():
#     root = tk.Tk()
#     root.geometry("1200x900")
#     root.title("Robox Robotics AI Kit")
#     root.configure(bg="#F8F9FA")

#     setup_styles()

#     # Create log queue for thread-safe logging
#     log_queue = queue.Queue()

#     # Create main layout
#     sidebar = ttk.Frame(root, style="Sidebar.TFrame", width=300)
#     sidebar.pack(side='left', fill='y')
#     sidebar.pack_propagate(False)

#     # Main area
#     main_area = ttk.Frame(root, style="Main.TFrame")
#     main_area.pack(side='right', fill='both', expand=True)

#     # Split main_area into top and bottom frames using pack
#     top_area = ttk.Frame(main_area, style="Main.TFrame")
#     top_area.pack(side='top', fill='both', expand=True)

#     log_area = ttk.Frame(main_area, style="Main.TFrame")
#     log_area.pack(side='bottom', fill='x')

#     # Label for log area
#     log_label = ttk.Label(log_area, text="Real-time Launch Output", style="Mode.TLabelframe.Label")
#     log_label.pack(anchor="w", padx=8, pady=(4, 0))

#     # Text widget for logs with scrollbar
#     log_frame = tk.Frame(log_area, bg="#F0F0F0")
#     log_frame.pack(fill='x', padx=8, pady=6)

#     log_text = tk.Text(log_frame, height=12, bg="#F0F0F0", relief="solid", bd=1, wrap=tk.WORD)
#     scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=log_text.yview)
#     log_text.configure(yscrollcommand=scrollbar.set)
    
#     log_text.pack(side=tk.LEFT, fill='both', expand=True)
#     scrollbar.pack(side=tk.RIGHT, fill='y')

#     # Sidebar header
#     header_frame = tk.Frame(sidebar, bg="#404680", height=60)
#     header_frame.pack(fill='x', pady=0)
#     header_frame.pack_propagate(False)

#     title_label = tk.Label(header_frame, text="Robox Control", 
#                         font=("Helvetica", 16, "bold"), 
#                         bg="#404680", fg="#ECF0F1")
#     title_label.pack(pady=15)

#     create_sidebar_sections(sidebar, log_text, log_queue)

#     # Add welcome message to log
#     log_text.insert(tk.END, "Welcome to Robox Robotics AI Kit Control Panel\n")
#     log_text.insert(tk.END, "Select a mode and click Execute to begin\n")
#     log_text.insert(tk.END, "Real-time launch file output will appear below\n")
#     log_text.insert(tk.END, "=" * 50 + "\n")

#     # Start the log queue processor
#     root.after(100, process_log_queue, log_text, log_queue, root)
    
#     root.mainloop()


# if __name__ == '__main__':
#     main()











import tkinter as tk
from tkinter import font, ttk, messagebox
import subprocess
import os
import signal
import threading
import queue
import time
import serial.tools.list_ports
import cv2
from PIL import Image, ImageTk


class VideoFeed:
    def __init__(self, parent, video_source="/dev/video10"):
        self.parent = parent
        self.video_source = video_source
        self.vid = None
        self.running = False
        self.frame = None
        self.capture_thread = None
        
        # Initialize video capture with error handling
        self.init_video_capture()
        
        self.canvas = tk.Label(self.parent)
        self.canvas.pack(fill='both', expand=True)
        
        # Start capture and GUI update only if camera is available
        if self.vid and self.vid.isOpened():
            self.start_capture()
        else:
            # Show "No Camera" message
            self.show_no_camera_message()

    def init_video_capture(self):
        """Initialize video capture with better error handling"""
        try:
            self.vid = cv2.VideoCapture(self.video_source)
            if self.vid.isOpened():
                # Set buffer size to prevent lag
                self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                # Test if we can actually read a frame
                ret, test_frame = self.vid.read()
                if not ret:
                    print(f"❌ Could not read from video source {self.video_source}")
                    if self.vid:
                        self.vid.release()
                        self.vid = None
                else:
                    print(f"✅ Video source {self.video_source} initialized successfully")
            else:
                print(f"❌ Could not open video source {self.video_source}")
                self.vid = None
        except Exception as e:
            print(f"❌ Error initializing video capture: {e}")
            self.vid = None

    def show_no_camera_message(self):
        """Show a message when camera is not available"""
        self.canvas.config(text="Camera not available", 
                          bg="#f0f0f0", 
                          fg="#666666",
                          font=("Helvetica", 14))

    def start_capture(self):
        """Start video capture in a separate thread"""
        self.running = True
        self.capture_thread = threading.Thread(target=self.capture_loop, daemon=True)
        self.capture_thread.start()
        self.update_gui()

    def capture_loop(self):
        """Video capture loop - runs in separate thread"""
        while self.running and self.vid and self.vid.isOpened():
            try:
                ret, frame = self.vid.read()
                if ret:
                    self.frame = frame
                else:
                    self.frame = None
                    break
                # Control frame rate and prevent CPU overload
                time.sleep(0.033)  # ~30 FPS
            except Exception as e:
                print(f"Error in capture loop: {e}")
                break
        
        # Cleanup if loop exits
        if self.vid:
            self.vid.release()
            self.vid = None

    def update_gui(self):
        """Update GUI with latest frame - runs in main thread"""
        if not self.running:
            return
            
        try:
            if self.frame is not None:
                # Resize frame to prevent memory issues
                height, width = self.frame.shape[:2]
                max_width = 640
                if width > max_width:
                    scale = max_width / width
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    frame = cv2.resize(self.frame, (new_width, new_height))
                else:
                    frame = self.frame
                
                # Convert and display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.imgtk = imgtk
                self.canvas.config(image=imgtk, text="")
        except Exception as e:
            print(f"Error updating GUI: {e}")
        
        # Schedule next update
        if self.running:
            self.parent.after(50, self.update_gui)  # 20 FPS for GUI updates

    def release(self):
        """Safely release video resources"""
        self.running = False
        
        # Wait for capture thread to finish
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        
        # Release video capture
        if self.vid and self.vid.isOpened():
            self.vid.release()
            self.vid = None
        
        print("Video feed released")


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
        if not self.is_connected:  # Only continue if still disconnected
            self.blink_state = not self.blink_state
            self.draw_led()
            self.blink_job = self.after(500, self.start_blinking)


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
        
        # Configure background to match parent
        self.configure(bg=parent.cget('bg'))
        
        self.draw_button()
        
        # Bind events
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def draw_button(self):
        self.delete("all")
        color = self.bg_color if self.enabled else "#CCCCCC"
        
        # Draw rounded rectangle
        self.create_rounded_rectangle(2, 2, self.width-2, self.height-2, 
                                    self.corner_radius, fill=color, outline="")
        
        # Draw text
        text_color = self.text_color if self.enabled else "#666666"
        self.create_text(self.width//2, self.height//2, text=self.text, 
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
            try:
                self.command()
            except Exception as e:
                print(f"Error in button command: {e}")
            
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
                   padding=20)

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


def log_output_reader(process, mode_name, log_queue, stop_event):
    """Thread function to read process output and put it in queue"""
    try:
        while not stop_event.is_set():
            if process.poll() is not None:
                break
                
            try:
                # Use a timeout to prevent blocking
                import select
                ready, _, _ = select.select([process.stdout], [], [], 0.1)
                if ready:
                    output = process.stdout.readline()
                    if output:
                        log_queue.put((mode_name, "stdout", output.strip()))
                    else:
                        break
            except:
                # Fallback for systems without select
                try:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        log_queue.put((mode_name, "stdout", output.strip()))
                except:
                    break
        
        # Read any remaining stderr
        try:
            stderr_output = process.stderr.read()
            if stderr_output:
                log_queue.put((mode_name, "stderr", stderr_output.strip()))
        except:
            pass
            
    except Exception as e:
        log_queue.put((mode_name, "error", f"Error reading output: {str(e)}"))


def process_log_queue(log_text, log_queue, root):
    """Process items from the log queue and update the text widget"""
    try:
        processed_count = 0
        while processed_count < 10:  # Limit processing to prevent GUI freezing
            try:
                mode_name, stream_type, message = log_queue.get_nowait()
                
                # Add timestamp and format message
                if stream_type == "stdout":
                    log_text.insert(tk.END, f"[{mode_name}] {message}\n")
                elif stream_type == "stderr":
                    log_text.insert(tk.END, f"[{mode_name}] ERROR: {message}\n")
                elif stream_type == "error":
                    log_text.insert(tk.END, f"[{mode_name}] SYSTEM ERROR: {message}\n")
                elif stream_type == "info":
                    log_text.insert(tk.END, f"[{mode_name}] INFO: {message}\n")
                
                processed_count += 1
                
            except queue.Empty:
                break
        
        # Auto-scroll to bottom
        log_text.see(tk.END)
        
        # Limit log size (keep last 1000 lines)
        try:
            lines = log_text.get("1.0", tk.END).split('\n')
            if len(lines) > 1000:
                log_text.delete("1.0", f"{len(lines)-1000}.0")
        except:
            pass
                
    except Exception as e:
        print(f"Error processing log queue: {e}")
    
    # Schedule next check
    if root.winfo_exists():
        root.after(100, process_log_queue, log_text, log_queue, root)


def operate(command, selected_mode, process_handles, log_text, log_queue, stop_events):
    print(f"🚀 Launching: {command}")
    log_text.insert(tk.END, f"🚀 Launching: {selected_mode}\n")
    log_text.see(tk.END)
    
    try:
        proc = subprocess.Popen(
            ["bash", "-c", command],
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )
        process_handles[selected_mode] = proc
        
        # Create stop event for this process
        stop_event = threading.Event()
        stop_events[selected_mode] = stop_event
        
        # Start thread to read output
        output_thread = threading.Thread(
            target=log_output_reader, 
            args=(proc, selected_mode, log_queue, stop_event),
            daemon=True
        )
        output_thread.start()
        
        log_text.insert(tk.END, f"✅ {selected_mode} started successfully\n")
        log_text.insert(tk.END, f"📋 Logging output from {selected_mode}...\n")
        
    except Exception as e:
        log_text.insert(tk.END, f"❌ Error starting {selected_mode}: {str(e)}\n")
    log_text.see(tk.END)

    
def activate_b(selected_mode, process_handles, stacking_combos, tracking_subwidgets, execute_buttons, log_text, log_queue, stop_events):
    print(f"▶️ Executing {selected_mode}")
    log_text.insert(tk.END, f"▶️ Executing {selected_mode}\n")
    log_text.see(tk.END)
    
    launch_commands = {
        "Color Sorting": "source /opt/ros/jazzy/setup.bash && source /home/saber/robox_ws/install/setup.bash && ros2 launch dashboard color_sorting.launch.py",
        "Color Stacking": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard color_stacking.launch.py",
        "Color Tracking": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard color_tracking.launch.py",
        "QR Detection": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard qr.launch.py",
        "Joystick": ". ~/robox_ws/install/setup.bash && ros2 launch dashboard joystick.launch.py"
    }
    
    # Stop existing processes
    for mode, proc in list(process_handles.items()):
        if proc.poll() is None:
            print(f"🛑 Stopping {mode}")
            log_text.insert(tk.END, f"🛑 Stopping {mode}\n")
            log_text.see(tk.END)
            
            # Signal stop event
            if mode in stop_events:
                stop_events[mode].set()
            
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                # Give process time to terminate gracefully
                time.sleep(0.5)
                if proc.poll() is None:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except:
                pass
    
    process_handles.clear()
    stop_events.clear()

    # Launch command
    if selected_mode in launch_commands:
        command = launch_commands[selected_mode]
        
        # Validate Stacking mode inputs
        if selected_mode == "Color Stacking":
            selected_values = [combo.get() for combo in stacking_combos.values()]
            if "" in selected_values:
                messagebox.showerror("Incomplete", "Please select a priority for each color.")
                return
            if len(set(selected_values)) != len(selected_values):
                messagebox.showerror("Duplicate Priority", "Each priority must be unique.")
                return
            final_priorities = {color: stacking_combos[color].get() for color in stacking_combos}
            print("✔️ Stacking Priorities:", final_priorities)
            log_text.insert(tk.END, f"✔️ Stacking Priorities: {final_priorities}\n")
            log_text.see(tk.END)
            messagebox.showinfo("Executed", f"Stacking Mode started with priorities: {final_priorities}")
            operate(command, selected_mode, process_handles, log_text, log_queue, stop_events)
            activate_f(selected_mode, execute_buttons)

        elif selected_mode == "Color Tracking":
            selected_color = None
            for color, btn in tracking_subwidgets.items():
                if btn.instate(["selected"]):
                    selected_color = color
                    print(f"Tracking color: {color}")
                    log_text.insert(tk.END, f"Tracking color: {color}\n")
                    log_text.see(tk.END)
                    break
            
            if selected_color:
                send_tracking_param(selected_color, log_text)
                operate(command, selected_mode, process_handles, log_text, log_queue, stop_events)
                activate_f(selected_mode, execute_buttons)
            else:
                messagebox.showerror("Error", "Please select a color to track")
                return
        else:        
            operate(command, selected_mode, process_handles, log_text, log_queue, stop_events)
            activate_f(selected_mode, execute_buttons)


def activate_f(selected_mode, execute_buttons):
    # Update button states
    for mode, btn in execute_buttons.items():
        if mode == selected_mode:
            # Change to running state
            btn.text = "Running"
            btn.original_bg_color = "#27AE60"  # Green
            btn.bg_color = "#27AE60"
            btn.hover_color = "#229954"  # Darker green
            btn.set_enabled(True)
        else:
            btn.set_enabled(False)
        btn.draw_button()


def quit_b(process_handles, log_text, stop_events):
    print("▶️ Quitting all modes")
    log_text.insert(tk.END, "▶️ Quitting all modes\n")
    log_text.see(tk.END)

    for mode, proc in list(process_handles.items()):
        if proc.poll() is None:
            print(f"🛑 Stopping {mode}")
            log_text.insert(tk.END, f"🛑 Stopping {mode}\n")
            log_text.see(tk.END)
            
            # Signal stop event
            if mode in stop_events:
                stop_events[mode].set()
            
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                time.sleep(0.5)
                if proc.poll() is None:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except:
                pass
    
    process_handles.clear()
    stop_events.clear()
    log_text.insert(tk.END, "✅ All processes stopped\n")
    log_text.see(tk.END)


def quit_f(execute_buttons):
    # Re-enable all execute buttons and restore original state
    for btn in execute_buttons.values():
        btn.text = "Execute"
        btn.original_bg_color = "#4A90E2"  # Blue
        btn.bg_color = "#4A90E2"
        btn.hover_color = "#357ABD"  # Darker blue
        btn.set_enabled(True)
        btn.draw_button()


def clear_log(log_text):
    """Clear the log text widget"""
    log_text.delete("1.0", tk.END)
    log_text.insert(tk.END, "Log cleared\n")
    log_text.insert(tk.END, "=" * 50 + "\n")


def quit_btn(sidebar, process_handles, execute_buttons, log_text, log_queue, stop_events):
    # Button container
    button_container = tk.Frame(sidebar, bg="#404680")
    button_container.pack(pady=15, padx=15, fill='x')

    # Quit button
    quit_btn = RoundedButton(
        button_container,
        text="Quit",
        command=lambda: [quit_b(process_handles, log_text, stop_events), quit_f(execute_buttons)],
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
        command=lambda: clear_log(log_text),
        bg_color="#F39C12",
        hover_color="#E67E22",
        width=250,
        height=35
    )
    clear_btn.pack(pady=5)


def execute_btn(mode_frame, mode, execute_buttons, stacking_combos, process_handles, tracking_subwidgets, log_text, log_queue, stop_events):
    # Execute button
    button_frame = tk.Frame(mode_frame, bg="#EEEDED")
    button_frame.pack(pady=5, fill='x')

    execute_btn = RoundedButton(
        button_frame, 
        text="Execute",
        command=lambda m=mode: activate_b(
            m, process_handles, stacking_combos, tracking_subwidgets, execute_buttons, log_text, log_queue, stop_events),
        bg_color="#4A90E2",
        hover_color="#357ABD",
        width=150,
        height=35
    )
    execute_btn.pack(pady=3)

    execute_buttons[mode] = execute_btn


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


def send_tracking_param(color, log_text):
    command = f"source /opt/ros/jazzy/setup.bash && ros2 param set /color_pose_publisher target_color \"{color}\""
    print(f"🔧 Setting param: {command}")
    log_text.insert(tk.END, f"🔧 Setting target_color = {color}\n")

    try:
        result = subprocess.run(
            ["bash", "-c", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10  # Add timeout to prevent hanging
        )

        if result.returncode == 0:
            log_text.insert(tk.END, f"✅ {result.stdout}\n")
        else:
            log_text.insert(tk.END, f"❌ {result.stderr}\n")

    except subprocess.TimeoutExpired:
        log_text.insert(tk.END, f"❌ Timeout setting parameter\n")
    except Exception as e:
        log_text.insert(tk.END, f"❌ Exception: {str(e)}\n")

    log_text.see(tk.END)


def create_sidebar_sections(sidebar, log_text, log_queue, stop_events):
    # Create mode sections
    stacking_combos = {}
    tracking_subwidgets = {}
    process_handles = {}
    execute_buttons = {}

    modes = ["Color Sorting", "Color Stacking", "Color Tracking", "QR Detection", "Joystick"]
    for mode in modes:
        mode_container = tk.Frame(sidebar, bg="#404680")
        mode_container.pack(pady=6, padx=12, fill='x')

        mode_frame = ttk.LabelFrame(mode_container, 
                                    text=mode, 
                                    style="Mode.TLabelframe",
                                    padding=6)
        mode_frame.pack(fill='x')

        # Mode-specific widgets
        if mode == "Color Stacking":
            stacking_combos.update(build_color_stacking_widgets(mode_frame))
        elif mode == "Color Tracking":
            build_color_tracking_widgets(mode_frame, tracking_subwidgets)

        execute_btn(mode_frame, mode, execute_buttons, stacking_combos, process_handles, tracking_subwidgets, log_text, log_queue, stop_events)

    quit_btn(sidebar, process_handles, execute_buttons, log_text, log_queue, stop_events)


def main():
    root = tk.Tk()
    root.geometry("1200x1000")
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

    video_frame = ttk.LabelFrame(top_area, text="Live Camera Feed", style="Mode.TLabelframe", padding=6)
    video_frame.pack(side='top', fill='both', expand=True, padx=8, pady=8)

    video_feed = VideoFeed(video_frame, video_source="/dev/video10")



    log_area = ttk.Frame(main_area, style="Main.TFrame")
    log_area.pack(side='bottom', fill='x')

    # Label for log area
    log_label = ttk.Label(log_area, text="Real-time Launch Output", style="Mode.TLabelframe.Label")
    log_label.pack(anchor="w", padx=8, pady=(4, 0))

    # Text widget for logs with scrollbar
    log_frame = tk.Frame(log_area, bg="#F0F0F0")
    log_frame.pack(fill='x', padx=8, pady=6)

    log_text = tk.Text(log_frame, height=12, bg="#F0F0F0", relief="solid", bd=1, wrap=tk.WORD)
    scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=log_text.yview)
    log_text.configure(yscrollcommand=scrollbar.set)
    
    log_text.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    # Sidebar header
    header_frame = tk.Frame(sidebar, bg="#404680", height=60)
    header_frame.pack(fill='x', pady=0)
    header_frame.pack_propagate(False)

    title_label = tk.Label(header_frame, text="Robox Control", 
                        font=("Helvetica", 16, "bold"), 
                        bg="#404680", fg="#ECF0F1")
    title_label.pack(pady=15)

    create_sidebar_sections(sidebar, log_text, log_queue)

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
        # Stop all processes and detection before closing
        root.quit()
        root.destroy()
        video_feed.release()  # Release video capture device

    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()