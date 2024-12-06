from djitellopy import Tello
import time

def fly_hexagon():
    # Initialize the Tello drone
    tello = Tello()
    
    # Connect to the drone
    tello.connect()
    print(f"Battery level: {tello.get_battery()}%")

    # Take off
    tello.takeoff()
    
    try:

        # Set altitude
        tello.move_up(80) 
        time.sleep(1)

        # Set the distance to travel for each side (in cm)
        distance = 300  
        
        # Hexagonal flight path
        for _ in range(6):
            tello.move_forward(distance)
            time.sleep(1)
            tello.rotate_clockwise(60)
            time.sleep(1)
        
    finally:
        # Land the drone safely
        tello.land()
        print("Flight completed!")

if __name__ == "__main__":
    fly_hexagon()    
