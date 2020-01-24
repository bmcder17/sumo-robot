#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import random
# Write your program here
brick.sound.beep()

# Object declarations
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
fun_motor = Motor(Port.C)
color_sensor = ColorSensor(Port.S1)
front_sensor = TouchSensor(Port.S2)
back_sensor = TouchSensor(Port.S3)
watch = StopWatch()

# Variable declarations
run = True
speed = 300
super_speed = 2 * speed
edge_threshold_nolop = 7
edge_threshold_blake = 7
# Function declarations
# Movement
def forward():
    right_motor.run(speed)
    left_motor.run(speed)
    return
    
def forward_time(time):
    right_motor.run_time(speed, time, Stop.COAST, False)
    left_motor.run_time(speed, time)
    return

def soft_stop():
    right_motor.stop()
    left_motor.stop()
    return

def stop():
    right_motor.stop(Stop.BRAKE)
    left_motor.stop(Stop.BRAKE)
    return
    
def reverse():
    right_motor.run_time(-(speed),2000, Stop.COAST, False)
    left_motor.run_time(-(speed),2000, Stop.COAST, True)
    return

def reverse_time(time):
    right_motor.run_time(-(speed),time, Stop.COAST, False)
    left_motor.run_time(-(speed),time, Stop.COAST, True)
    return
    

def turn_180_in_place():
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    left_motor.run_target(speed, 480, Stop.COAST, False)
    right_motor.run_target(-(speed), -480, Stop.COAST, True)
    return

def turn_90_in_place():
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    left_motor.run_target(speed, 240, Stop.COAST, False)
    right_motor.run_target(-(speed), -240, Stop.COAST, True)
    return

def turn_180(num):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    if (num == 0):
        left_motor.run_angle(speed, 960, Stop.COAST, True)
    elif (num == 1):
        right_motor.run_angle(speed, 960, Stop.COAST, True)
    return

def turn_90(num):
    left_motor.reset_angle(0)
    right_motor.reset_angle(0)
    if (num == 0):
         left_motor.run_angle(super_speed, 480, Stop.COAST, True)
    elif (num == 1):
         right_motor.run_angle(super_speed, 480, Stop.COAST, True)
    return


# safety checks (edge detection)
def edge_detection():
    edge_light = color_sensor.reflection()
    if edge_light < edge_threshold_blake:
        reverse()
        turn_180_in_place()
        forward()
        return True
    return False

def front_detection():
    if front_sensor.pressed():
        right_motor.run(super_speed)
        left_motor.run(super_speed)
        return True
    return False
        
def back_detection():
    if back_sensor.pressed():
        num = random.randint(0,1)
        turn_90(num)
        forward()
        return True
    return False

# standby    
while not (Button.LEFT in brick.buttons()):
    pass

# startup
brick.sound.file('/home/robot/Sumo_robot/pacman_beginning.wav')
forward()
fun_motor.run(250)
watch.reset()

# main running loop
while run:
    if (edge_detection()):
        watch.reset()
    if (back_detection()):
        watch.reset()
    if (front_detection()):
        watch.reset()
    if (watch.time() >= 15000):
        randMove = random.randint(0,5)
        if (randMove == 0):
            time = random.randint(1,3) * 1000
            forward_time(time)
        elif (randMove == 1):
            dir = random.randint(0,1)
            turn_90(dir)
        elif (randMove == 2):
            dir = random.randint(0,1)
            turn_180(dir)
        elif (randMove == 3):
            dir = random.randint(0,1)
            turn_90_in_place(dir)
        elif (randMove == 4):
            dir = random.randint(0,1)
            turn_180_in_place(dir)
        elif (randMove == 5):
            time = random.randint(1,3) * 1000
        forward()
        watch.reset()
    if (right_motor.speed() == 0 and left_motor.speed() == 0):
        forward()
    if (Button.RIGHT in brick.buttons()):
        run = False
