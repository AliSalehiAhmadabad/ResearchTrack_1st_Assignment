from __future__ import print_function
import time
from sr.robot import *

ANGLE_THRESHOLD = 2.0
DISTANCE_THRESHOLD = 0.4

robot = Robot()
collected_boxes = list()

def set_velocity(linear_speed, angular_speed, duration):
    robot.motors[0].m0.power = linear_speed + angular_speed
    robot.motors[0].m1.power = linear_speed - angular_speed
    time.sleep(duration)
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0

def find_closest_box(marker_type, is_collected):
    closest_distance = 100
    closest_rotation = 0
    closest_code = -1
    
    for box in robot.see():
        if box.dist < closest_distance and box.info.marker_type == marker_type and box.info.code not in collected_boxes and (not is_collected or box.info.code in collected_boxes):
            closest_distance = box.dist
            closest_rotation = box.rot_y
            closest_code = box.info.code
    
    if closest_distance == 100:
        return -1, -1, -1
    
    return closest_distance, closest_rotation, closest_code

def approach_box(distance_threshold, rotation_threshold, marker_type, is_collected, action_description):
    is_found = True
    while is_found:
        distance, rotation, code = find_closest_box(marker_type, is_collected)
        if distance < distance_threshold:
            print(f"Box Found: {action_description}")
            is_found = False
        elif -rotation_threshold <= rotation <= rotation_threshold:
            print(f"Approaching the box: {action_description}")
            set_velocity(10, 0, 0.5)
        elif rotation < -rotation_threshold:
            print(f"Adjusting position: Move left - {action_description}")
            set_velocity(0, 2, 0.5)
        elif rotation > rotation_threshold:
            print(f"Adjusting position: Move right - {action_description}")
            set_velocity(0, -2, 0.5)

def main():
    distance, rotation, code = find_closest_box(MARKER_TOKEN_GOLD, False)
    
    while distance == -1:
        print("No Golden Box in sight. Searching...")
        set_velocity(0, 5, 2)
        distance, rotation, code = find_closest_box(MARKER_TOKEN_GOLD, False)

    approach_box(DISTANCE_THRESHOLD, ANGLE_THRESHOLD, MARKER_TOKEN_GOLD, False, "Attempting to collect the Golden Box")
    robot.grab()
    print("Golden Box Collected Successfully!")

    set_velocity(-10, 0, 1.1)
    set_velocity(10, 0, 19)
    robot.release()
    print("Delivery Completed!")

    set_velocity(-10, 0, 2)
    set_velocity(0, 30, 2)
    collected_boxes.append(code)

    while len(collected_boxes) < 6:
        distance, rotation, code = find_closest_box(MARKER_TOKEN_GOLD, False)
        while distance == -1:
            print("No Golden Box in sight. Searching...")
            set_velocity(0, 5, 2)
            distance, rotation, code = find_closest_box(MARKER_TOKEN_GOLD, False)
        approach_box(DISTANCE_THRESHOLD, ANGLE_THRESHOLD, MARKER_TOKEN_GOLD, False, "Attempting to collect the Golden Box")
        robot.grab()
        print("Golden Box Collected Successfully!")

        new_distance, new_rotation, new_code = find_closest_box(MARKER_TOKEN_GOLD, True)
        while new_distance == -1:
            print("No drop location in sight. Searching...")
            set_velocity(0, 5, 2)
            new_distance, new_rotation, new_code = find_closest_box(MARKER_TOKEN_GOLD, True)
        approach_box(DISTANCE_THRESHOLD, ANGLE_THRESHOLD, MARKER_TOKEN_GOLD, True, "Releasing the Golden Box")
        robot.release()
        print("Delivery Completed!")
        set_velocity(-10, 0, 2)
        set_velocity(0, 30, 2)
        collected_boxes.append(new_code)

# Execute the main function
main()
