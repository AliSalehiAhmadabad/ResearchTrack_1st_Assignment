from __future__ import print_function
import time
from sr.robot import *

angle_threshold = 2.0
""" float: Threshold for the control of the orientation"""

distance_threshold = 0.4
""" float: Threshold for the control of the linear distance"""

robot_instance = Robot()
""" instance of the class Robot"""

def set_linear_velocity(speed, seconds):
    """
    Function for setting a linear velocity

    Args:
        speed (int): the speed of the wheels
        seconds (int): the time interval
    """
    robot_instance.motors[0].m0.power = speed
    robot_instance.motors[0].m1.power = speed
    time.sleep(seconds)
    robot_instance.motors[0].m0.power = 0
    robot_instance.motors[0].m1.power = 0

def set_angular_velocity(speed, seconds):
    """
    Function for setting an angular velocity

    Args:
        speed (int): the speed of the wheels
        seconds (int): the time interval
    """
    robot_instance.motors[0].m0.power = speed
    robot_instance.motors[0].m1.power = -speed
    time.sleep(seconds)
    robot_instance.motors[0].m0.power = 0
    robot_instance.motors[0].m1.power = 0

def find_closest_gold_token():
    """
    Function to find the closest golden token

    Returns:
        distance (float): distance of the closest golden token (-1 if no token is detected)
        rotation (float): angle between the robot and the golden token (-1 if no token is detected)
    """
    closest_distance = 100

    for box in robot_instance.see():
        if box.dist < closest_distance and box.info.marker_type == MARKER_TOKEN_GOLD:
            closest_distance = box.dist
            rotation = box.rot_y

    if closest_distance == 100:
        return -1, -1
    else:
        return closest_distance, rotation

loop_counter = 1

while loop_counter:
    distance, rotation = find_closest_gold_token()

    while distance == -1:
        print("Searching for tokens...")
        set_angular_velocity(7, 0.4)
        distance, rotation = find_closest_gold_token()

    if distance < distance_threshold:
        print("Token located!")
        robot_instance.grab()
        print("Token captured!")
        loop_counter = 0
    elif -angle_threshold <= rotation <= angle_threshold:
        print("Moving forward.")
        set_linear_velocity(12, 0.7)
    elif rotation < -angle_threshold:
        print("Adjusting position: Left.")
        set_angular_velocity(-3, 0.35)
    elif rotation > angle_threshold:
        print("Adjusting position: Right.")
        set_angular_velocity(3, 0.35)

set_angular_velocity(-12, 1)
set_linear_velocity(90, 2)
robot_instance.release()

set_linear_velocity(-60, 0.5)
set_angular_velocity(-40, 1)
set_linear_velocity(40, 1)

loop_counter2 = 0

while loop_counter2 < 5:
    distance, rotation = find_closest_gold_token()

    while distance == -1:
        print("Searching for tokens...")
        set_angular_velocity(7, 0.4)
        distance, rotation = find_closest_gold_token()

    if distance < distance_threshold:
        print("Token located!")
        robot_instance.grab()
        print("Token captured!")
        set_angular_velocity(50, 1)
        set_linear_velocity(66, 2)

        robot_instance.release()
        set_linear_velocity(-20, 1.5)
        set_angular_velocity(-40, 1)
        set_linear_velocity(40, 1)
        loop_counter2 += 1
    elif -angle_threshold <= rotation <= angle_threshold:
        print("Moving forward.")
        set_linear_velocity(12, 0.7)
    elif rotation < -angle_threshold:
        print("Adjusting position: Left.")
        set_angular_velocity(-3, 0.35)
    elif rotation > angle_threshold:
        print("Adjusting position: Right.")
        set_angular_velocity(3, 0.35)
