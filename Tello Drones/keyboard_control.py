from djitellopy import Tello
from pynput.keyboard import Listener, Key
import cv2
import threading
import time

# Initialize Tello drone
tello = Tello()
tello.connect()
print(f"Battery level: {tello.get_battery()}%")

# Start video stream
tello.streamon()
frame_reader = tello.get_frame_read()

# Tracking flight state
is_flying = False
key_state = {
    'w': False,  
    's': False,  
    'a': False,  
    'd': False, 
    'q': False, 
    'e': False,
    'up': False,
    'down': False,
    'left': False,
    'right': False,
}

def handle_key_press(key):
    """Handles key press events."""
    global is_flying

    try:
        if hasattr(key, 'char') and key.char in key_state:
            key_state[key.char] = True
        elif key == Key.up:
            key_state['up'] = True
        elif key == Key.down:
            key_state['down'] = True
        elif key == Key.space:
            if not is_flying:
                tello.takeoff()
                is_flying = True
                print("Drone is airborne!")
            else:
                tello.land()
                is_flying = False
                print("Drone has landed.")
    except Exception as e:
        print(f"Error in key press handling: {e}")

def handle_key_release(key):
    """Handles key release events."""
    try:
        if hasattr(key, 'char') and key.char in key_state:
            key_state[key.char] = False
        elif key == Key.up:
            key_state['up'] = False
        elif key == Key.down:
            key_state['down'] = False
        elif key == Key.esc:
            if is_flying:
                tello.land()
                print("Drone landed safely.")
            tello.streamoff()
            print("Exiting program...")
            return False  # Stops the listener
    except Exception as e:
        print(f"Error in key release handling: {e}")

def process_drone_movement():
    """Continuously sends commands to the drone based on key states."""
    global key_state, is_flying

    while True:
        if is_flying:
            # Default values for movement
            lr = 0  # Left/Right
            fb = 0  # Forward/Backward
            ud = 0  # Up/Down
            yaw = 0  # Rotate

            # Update based on key states
            if key_state['w']:
                fb = 30
            elif key_state['s']:
                fb = -30
            if key_state['a']:
                lr = -30
            elif key_state['d']:
                lr = 30
            if key_state['up']:
                ud = 30
            elif key_state['down']:
                ud = -30
            if key_state['q']:
                yaw = -30 
            elif key_state['e']:
                yaw = 30

            # Send the control command
            try:
                tello.send_rc_control(lr, fb, ud, yaw)
            except Exception as e:
                print(f"Error sending control command: {e}")
        
        time.sleep(0.05)  # Adjust loop frequency for responsiveness

def start_video_feed():
    """Displays the video feed from the Tello drone."""
    while True:
        # Get the latest frame
        frame = frame_reader.frame

        # Display the video feed
        cv2.imshow("Tello Video Feed", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            tello.streamoff()
            cv2.destroyAllWindows()
            break

def start_keyboard_control():
    """Starts the keyboard listener for drone control."""
    with Listener(on_press=handle_key_press, on_release=handle_key_release) as listener:
        listener.join()

if __name__ == "__main__":
    print("Keyboard control started. Use the following keys:")
    print("W/S: Move forward/backward")
    print("A/D: Move left/right")
    print("Q/E: Rotate counterclockwise/clockwise")
    print("Arrow Keys: Move up/down")
    print("Space: Take off/land")
    print("Esc: Land and exit")
    print("Press 'Q' to close the video feed window.")

    # Start video feed in a separate thread
    video_thread = threading.Thread(target=start_video_feed, daemon=True)
    video_thread.start()

    # Start drone movement processing thread
    movement_thread = threading.Thread(target=process_drone_movement, daemon=True)
    movement_thread.start()

   
    start_keyboard_control()
