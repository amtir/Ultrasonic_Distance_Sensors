#!/usr/bin/env python3


import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



#TRIG = [2,3,4,14,15,18,17,27]   # GPIO Output Pins to trigger the Ultrasonic sensor
#ECHO = [22,23,24,10,9,11,25,8]  # GPIO Input Pins to listen to incoming wave-sound
#Wave_Distance = [0,0,0,0,0,0,0,0] # Wave distance in cm

#-----------------------------------------------
def set_trigger_pins(TRIG):
    print("Setting the TRIG GPIO OUTPUT in progress ...")
    try:
        for i in range(len(TRIG)):
            GPIO.setup(TRIG[i],GPIO.OUT)
    except Exception as e:
        print("-> [-] TRIG.")
        print("Error setting GPIO OUTPUT: {}".format(e))
        sys.exit(0)
    else:
        print(" -> [+] TRIG.\n")

#---------------------------------------------
def set_echo_pins(ECHO):
    print("Setting the ECHO GPIO INPUT ...")
    try:
        for i in range(len(ECHO)):
            GPIO.setup(ECHO,GPIO.IN)
    except Exception as e:
        print("Error setting GPIO INPUT - ECHO.")
        print(e)
        sys.exit(0)
    else:
        print(" -> [+] ECHO.\n")

#----------------------------------------------
def init_trigger(TRIG):
    print("Setting the TRIG GPIO OUTPUT to LOW ...")
    try:
        for i in range(len(TRIG)):
            GPIO.output(TRIG, False)
    except Exception as e:
        print("Error setting GPIO OUTPUT - TRIG.")
        print(e)
        sys.exit(0)
    else:
        #print("Waiting For Sensor To Settle")
        time.sleep(1)
        print(" -> [+] TRIG set to LOW.\n")

#-------------------------------------------
