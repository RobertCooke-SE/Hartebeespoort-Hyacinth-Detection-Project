from djitellopy import Tello
import time

def perform_tricks():
    tello = Tello()
    tello.connect()

    print(f"Battery level: {tello.get_battery()}%")

    # Take off
    tello.takeoff()
    time.sleep(2) 

    try:

         # Set altitude
        tello.move_up(40) 
        time.sleep(1)


        tello.flip_forward()
        time.sleep(1)

        tello.flip_back()
        time.sleep(1)

        tello.flip_left()
        time.sleep(1)

        tello.flip_right()
        time.sleep(1)

        
    finally:
        # Land the drone safely
        tello.land()
        print("Drone has landed.")

if __name__ == "__main__":
    perform_tricks()
