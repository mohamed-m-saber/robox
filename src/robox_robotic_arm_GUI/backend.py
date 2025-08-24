import subprocess
import os
import signal
import threading
import queue
import tkinter as tk
from tkinter import messagebox
import pygame
import serial.tools.list_ports
import time

class DeviceDetector:
    def __init__(self, arduino_led, joystick_led, log_text, log_queue):
        self.arduino_led = arduino_led
        self.joystick_led = joystick_led
        self.log_text = log_text
        self.log_queue = log_queue
        self.detection_thread = None
        self.stop_detection = False

        # Camera capture object
        self.cap = None
        
        # Initialize pygame for joystick detection
        self.pygame_initialized = False
        self.init_pygame()

        self.prev_arduino_state = None
        self.prev_camera_state = None
        self.prev_joystick_state = None

    def init_pygame(self):
        """Initialize pygame for joystick detection"""
        try:
            pygame.init()
            pygame.joystick.init()
            self.pygame_initialized = True
            self.log_queue.put(("System", "info", "Pygame initialized for joystick detection"))
        except Exception as e:
            self.log_queue.put(("System", "error", f"Failed to initialize pygame: {str(e)}"))
            self.pygame_initialized = False

    def check_arduino_connection(self):
        try:
            ports = serial.tools.list_ports.comports()
            arduino_ports = [port for port in ports if 'Arduino' in port.description or 
                             'CH340' in port.description or 'USB' in port.description]
            return len(arduino_ports) > 0
        except Exception as e:
            self.log_queue.put(("System", "error", f"Arduino detection error: {str(e)}"))
            return False

    def check_joystick_connection(self):
        """Check if any joystick/gamepad is connected"""
        if not self.pygame_initialized:
            return False
        
        try:
            # Update pygame joystick list
            pygame.joystick.quit()
            pygame.joystick.init()
            
            joystick_count = pygame.joystick.get_count()
            return joystick_count > 0
        except Exception as e:
            self.log_queue.put(("System", "error", f"Joystick detection error: {str(e)}"))
            return False

    def detect_devices(self):
        """Continuously detect devices in background thread"""
        while not self.stop_detection:
            try:
                # Check Arduino
                arduino_connected = self.check_arduino_connection()
                if arduino_connected != self.prev_arduino_state:
                    self.arduino_led.set_connected(arduino_connected)
                    status = "connected" if arduino_connected else "disconnected"
                    self.log_queue.put(("System", "info", f"Arduino {status}"))
                    self.prev_arduino_state = arduino_connected

 

                # Check Joystick
                joystick_connected = self.check_joystick_connection()
                if joystick_connected != self.prev_joystick_state:
                    self.joystick_led.set_connected(joystick_connected)
                    status = "connected" if joystick_connected else "disconnected"
                    self.log_queue.put(("System", "info", f"Joystick {status}"))
                    
                    # Log joystick details when connected
                    if joystick_connected:
                        try:
                            joystick_count = pygame.joystick.get_count()
                            for i in range(joystick_count):
                                joystick = pygame.joystick.Joystick(i)
                                joystick.init()
                                joystick_name = joystick.get_name()
                                self.log_queue.put(("System", "info", f"Joystick detected: {joystick_name}"))
                                joystick.quit()
                        except Exception as e:
                            self.log_queue.put(("System", "error", f"Error getting joystick info: {str(e)}"))
                    
                    self.prev_joystick_state = joystick_connected

                time.sleep(2)

            except Exception as e:
                self.log_queue.put(("System", "error", f"Device detection error: {str(e)}"))
                time.sleep(5)

    def start_detection(self):
        """Start device detection in background thread"""
        if not self.detection_thread or not self.detection_thread.is_alive():
            # # Open camera once
            # self.cap = cv2.VideoCapture(2)
            # if not self.cap.isOpened():
            #     self.log_queue.put(("System", "error", "Failed to open camera"))
            #     self.cap = None
            # else:
            #     self.log_queue.put(("System", "info", "Camera capture opened successfully"))

            self.stop_detection = False
            self.detection_thread = threading.Thread(target=self.detect_devices, daemon=True)
            self.detection_thread.start()
            self.log_queue.put(("System", "info", "Device detection started"))

    def stop_detection_process(self):
        """Stop device detection"""
        self.stop_detection = True
        if self.detection_thread:
            self.detection_thread.join(timeout=1)

       

        # Quit pygame
        if self.pygame_initialized:
            try:
                pygame.joystick.quit()
                pygame.quit()
                self.log_queue.put(("System", "info", "Pygame cleanup completed"))
            except:
                pass



    def stop_detection_process(self):
        """Stop device detection"""
        self.stop_detection = True
        if self.detection_thread:
            self.detection_thread.join(timeout=1)

        # Release the camera if open
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.log_queue.put(("System", "info", "Camera capture released"))

        # Quit pygame
        if self.pygame_initialized:
            try:
                pygame.joystick.quit()
                pygame.quit()
                self.log_queue.put(("System", "info", "Pygame cleanup completed"))
            except:
                pass











def log_output_reader(process, mode_name, log_queue):
    """Thread function to read process output and put it in queue"""
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log_queue.put((mode_name, "stdout", output.strip()))
        
        # Read any remaining stderr
        stderr_output = process.stderr.read()
        if stderr_output:
            log_queue.put((mode_name, "stderr", stderr_output.strip()))
            
    except Exception as e:
        log_queue.put((mode_name, "error", f"Error reading output: {str(e)}"))





def process_log_queue(log_text, log_queue, root):
    """Process items from the log queue and update the text widget"""
    try:
        while True:
            mode_name, stream_type, message = log_queue.get_nowait()
            
            if stream_type == "stdout":
                log_text.insert(tk.END, f"[{mode_name}] {message}\n")
            elif stream_type == "stderr":
                log_text.insert(tk.END, f"[{mode_name}] ERROR: {message}\n")
            elif stream_type == "error":
                log_text.insert(tk.END, f"[{mode_name}] SYSTEM ERROR: {message}\n")
            
            # Auto-scroll to bottom
            log_text.see(tk.END)
            
            # Limit log size (keep last 1000 lines)
            lines = log_text.get("1.0", tk.END).split('\n')
            if len(lines) > 1000:
                log_text.delete("1.0", f"{len(lines)-1000}.0")
                
    except queue.Empty:
        pass
    except Exception as e:
        print(f"Error processing log queue: {e}")
    
    # Schedule next check
    root.after(100, process_log_queue, log_text, log_queue, root)


def send_tracking_param(color, log_text):
    command = f"source /opt/ros/jazzy/setup.bash && source /home/saber/robox_ws/install/setup.bash && ros2 param set /color_tracking_pub target_color {color.strip()}"
    print(f"🔧 Setting param: {command}")
    log_text.insert(tk.END, f"🔧 Setting target_color = {color.strip()}\n")

    try:
        result = subprocess.run(
            ["bash", "-c", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        log_text.insert(tk.END, f"📊 Return code: {result.returncode}\n")

        if result.returncode == 0:
            output = result.stdout.strip() or "✅ Parameter set successfully"
            log_text.insert(tk.END, f"✅ {output}\n")
            
            # Verify the parameter was set
            verify_command = f"source /opt/ros/jazzy/setup.bash && source /home/saber/robox_ws/install/setup.bash && ros2 param get /color_tracking_pub target_color"
            try:
                verify_result = subprocess.run(
                    ["bash", "-c", verify_command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                
                if verify_result.returncode == 0:
                    log_text.insert(tk.END, f"✅ Verification: {verify_result.stdout.strip()}\n")
                else:
                    log_text.insert(tk.END, f"⚠️ Verification failed: {verify_result.stderr.strip()}\n")
            except subprocess.TimeoutExpired:
                log_text.insert(tk.END, f"⏱️ Verification timed out\n")
                
        else:
            error_output = result.stderr.strip() or "❌ Unknown error occurred"
            log_text.insert(tk.END, f"❌ {error_output}\n")

    except subprocess.TimeoutExpired:
        log_text.insert(tk.END, f"⏱️ Command timed out\n")
    except Exception as e:
        log_text.insert(tk.END, f"❌ Exception: {str(e)}\n")

    log_text.see(tk.END)


def send_stacking_params(priorities, log_text):
    for color, priority in priorities.items():
        param_name = f"{color.lower().strip()}_priority"
        command = f"source /opt/ros/jazzy/setup.bash && source /home/saber/robox_ws/install/setup.bash && ros2 param set /ppc_action_client_stacking {param_name} {priority}"
        
        log_text.insert(tk.END, f"🔧 Setting {param_name} = {priority}\n")

        try:
            result = subprocess.run(
                ["bash", "-c", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )

            log_text.insert(tk.END, f"📊 Return code: {result.returncode}\n")

            if result.returncode == 0:
                output = result.stdout.strip() or "✅ Parameter set successfully"
                log_text.insert(tk.END, f"✅ {output}\n")
                
                # Verify the parameter was set
                verify_command = f"source /opt/ros/jazzy/setup.bash && source /home/saber/robox_ws/install/setup.bash && ros2 param get /ppc_action_client_stacking {param_name}"
                try:
                    verify_result = subprocess.run(
                        ["bash", "-c", verify_command],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=5
                    )
                    
                    if verify_result.returncode == 0:
                        log_text.insert(tk.END, f"✅ Verification: {verify_result.stdout.strip()}\n")
                    else:
                        log_text.insert(tk.END, f"⚠️ Verification failed: {verify_result.stderr.strip()}\n")
                except subprocess.TimeoutExpired:
                    log_text.insert(tk.END, f"⏱️ Verification timed out\n")
                    
            else:
                error_output = result.stderr.strip() or "❌ Unknown error occurred"
                log_text.insert(tk.END, f"❌ {error_output}\n")

        except subprocess.TimeoutExpired:
            log_text.insert(tk.END, f"⏱️ Command timed out\n")
        except Exception as e:
            log_text.insert(tk.END, f"❌ Exception: {str(e)}\n")

        log_text.see(tk.END)
        time.sleep(0.5)  # Small delay between parameter settings



def operate(command, selected_mode, process_handles, log_text, log_queue):
    """Start a new process and begin logging its output"""
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
        
        # Start thread to read output
        output_thread = threading.Thread(
            target=log_output_reader, 
            args=(proc, selected_mode, log_queue),
            daemon=True
        )
        output_thread.start()
        
        log_text.insert(tk.END, f"✅ {selected_mode} started successfully\n")
        log_text.insert(tk.END, f"📋 Logging output from {selected_mode}...\n")
        
    except Exception as e:
        log_text.insert(tk.END, f"❌ Error starting {selected_mode}: {str(e)}\n")
    log_text.see(tk.END)

def activate_b(selected_mode, process_handles, stacking_combos, tracking_subwidgets, execute_buttons, log_text, log_queue):
    print(f"▶️ Executing {selected_mode}")
    log_text.insert(tk.END, f"▶️ Executing {selected_mode}\n")
    log_text.see(tk.END)

    base_cmd = "source /opt/ros/jazzy/setup.bash && source ~/robox_ws/install/setup.bash"

    # Stop all currently running processes
    for mode, proc in process_handles.items():
        if proc.poll() is None:
            log_text.insert(tk.END, f"🛑 Stopping {mode}\n")
            os.killpg(os.getpgid(proc.pid), signal.SIGINT)
    process_handles.clear()

    if selected_mode == "Color Stacking":
        selected_values = [combo.get() for combo in stacking_combos.values()]
        if "" in selected_values:
            messagebox.showerror("Incomplete", "Please select a priority for each color.")
            return
        if len(set(selected_values)) != len(selected_values):
            messagebox.showerror("Duplicate Priority", "Each priority must be unique.")
            return

        priorities = {color: stacking_combos[color].get() for color in stacking_combos}
        launch_args = " ".join([
        f"{color.lower().strip()}_priority:={priority}"
        for color, priority in priorities.items()
    ])
        command = f"{base_cmd} && ros2 launch dashboard color_stacking.launch.py {launch_args}"

        log_text.insert(tk.END, f"✔️ Stacking Priorities: {priorities}\n")
        operate(command, selected_mode, process_handles, log_text, log_queue)
        activate_f(selected_mode, execute_buttons)
        messagebox.showinfo("Executed", f"Stacking Mode started with priorities: {priorities}")

    elif selected_mode == "Color Tracking":
        selected_color = None
        for color, btn in tracking_subwidgets.items():
            if btn.instate(["selected"]):
                selected_color = color
                break

        if not selected_color:
            messagebox.showerror("Error", "Please select a color to track")
            return

        # ✅ Correct launch argument passing (no --ros-args)
        command = f"{base_cmd} && ros2 launch dashboard color_tracking.launch.py target_color:={selected_color}"
        log_text.insert(tk.END, f"🎯 Tracking color: {selected_color}\n")
        operate(command, selected_mode, process_handles, log_text, log_queue)
        activate_f(selected_mode, execute_buttons)

    else:
        command = f"{base_cmd} && ros2 launch dashboard {selected_mode.lower().replace(' ', '_')}.launch.py"
        operate(command, selected_mode, process_handles, log_text, log_queue)
        activate_f(selected_mode, execute_buttons)

    log_text.see(tk.END)


def activate_f(selected_mode, execute_buttons):
    """Update button states after execution"""
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


def quit_b(process_handles, log_text):
    """Stop all running processes"""
    print("▶️ Quitting all modes")
    log_text.insert(tk.END, "▶️ Quitting all modes\n")
    log_text.see(tk.END)

    for mode, proc in process_handles.items():
        if proc.poll() is None:
            print(f"🛑 Stopping {mode}")
            log_text.insert(tk.END, f"🛑 Stopping {mode}\n")
            log_text.see(tk.END)
            os.killpg(os.getpgid(proc.pid), signal.SIGINT)
    process_handles.clear()
    log_text.insert(tk.END, "✅ All processes stopped\n")
    log_text.see(tk.END)


def quit_f(execute_buttons):
    """Re-enable all execute buttons and restore original state"""
    
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






