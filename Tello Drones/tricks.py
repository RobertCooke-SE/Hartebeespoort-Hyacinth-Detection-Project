from tkinter import Tk, Button, Label
from djitellopy import Tello
import time

tello = Tello()
tello.connect()
print(f"Battery level: {tello.get_battery()}%")

# Variable to track drone state
is_flying = False

def takeoff():
    """Take off the drone."""
    global is_flying
    if not is_flying:
        tello.takeoff()
        is_flying = True
        status_label.config(text="Status: Flying")

def land():
    """Land the drone."""
    global is_flying
    if is_flying:
        tello.land()
        is_flying = False
        status_label.config(text="Status: Landed")

def flip_forward():
    """Make the drone perform a forward flip."""
    if is_flying:
        tello.flip_forward()

def flip_back():
    """Make the drone perform a backward flip."""
    if is_flying:
        tello.flip_back()

def flip_left():
    """Make the drone perform a left flip."""
    if is_flying:
        tello.flip_left()

def flip_right():
    """Make the drone perform a right flip."""
    if is_flying:
        tello.flip_right()

def rotate_360():
    """Make the drone rotate 360 degrees."""
    if is_flying:
        for _ in range(6):  # Rotate in small increments for smoother rotation
            tello.rotate_clockwise(60)
            

def circle_flight(radius=50, steps=36):
    """
    Make the drone move in a circular trajectory.
    :param radius: Distance to move forward in each step (in cm).
    :param steps: Number of steps to complete the circle (higher = smoother).
    """
    if is_flying:
        angle_per_step = 360 // steps  # Degrees to turn per step
        for _ in range(steps):
            tello.move_forward(radius // steps)  # Move a portion of the radius
            tello.rotate_clockwise(angle_per_step)  # Rotate slightly
            time.sleep(0.5)  # Pause to ensure smooth execution


# Create the GUI
app = Tk()
app.title("DJI Tello Controller")

# Status Label
status_label = Label(app, text="Status: Ready", font=("Arial", 14))
status_label.pack(pady=10)

# Control Buttons
Button(app, text="Take Off", command=takeoff, width=20, bg="green").pack(pady=5)
Button(app, text="Land", command=land, width=20, bg="red").pack(pady=5)

Label(app, text="Tricks:", font=("Arial", 12)).pack(pady=10)
Button(app, text="Flip Forward", command=flip_forward, width=20).pack(pady=5)
Button(app, text="Flip Backward", command=flip_back, width=20).pack(pady=5)
Button(app, text="Flip Left", command=flip_left, width=20).pack(pady=5)
Button(app, text="Flip Right", command=flip_right, width=20).pack(pady=5)
Button(app, text="Rotate 360°", command=rotate_360, width=20).pack(pady=5)
Button(app, text="Circle Flight", command=lambda: circle_flight(100), width=20).pack(pady=5)


# Run the GUI
app.mainloop()
