#!/usr/bin/env python3


import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

from hcrsr04_lib import *


TRIG = [2,3,4,14,15,18,17,27]   # GPIO Output Pins to trigger the Ultrasonic sensor
ECHO = [22,23,24,10,9,11,25,8]  # GPIO Input Pins to listen to incoming wave-sound
Wave_Distance = [0,0,0,0,0,0,0,0] # Wave distance in cm

# The wave sound travels between the sensor and the drip tray.
# The distance between the sensor and the drip tray is around 30cm.
# The wave is reflected at the drip tray surface and returns-back to the sensor. 
# So the total distance is then d = 2 * 30cm = 60cm
# Knowing that the Sound speed is 343 m/s = 34300 cm/s at 20°C, we could estimate the travel time of the wave sound. d / sound_speed = 60 /34300 ~ 0.001745 ~ 1.75ms ~1.8ms
SOUND_WAVE_TRAVEL = 0.0025  # wave-sound travel (1.8ms) + Trigger (10Us) +  8 burst-pulses @40HZ (8x25Us=200Us) + etc ... =  ~2ms ~3ms )
WDT_bln = False             # WatchDog Boolean Flag

#-----------------------------------------------
#-------------------------------------------

#--------------------------------------------
def main():
    
    # Set and Initialisation of the I/O Trigger, Echo, ...
    set_trigger_pins(TRIG)
    set_echo_pins(ECHO)
    init_trigger(TRIG)
    
    print("Distance Measurement In Progress ...")
    while(True):
        
        t_start=time.time()
        strDistance = str(t_start)
        
        # Trigger signal - start the measurement ( -> 8 pulses - generate the sound waves)
        for i in range(len(TRIG)):
            GPIO.output(TRIG[i], True)
            time.sleep(0.00001)
            GPIO.output(TRIG[i], False)
            
            WDT_bln = False
            
            delta_time = 0
            distance = 0
            t_US_start = time.time()
            
            #Listen for the echo of the the wave sound
            while ( GPIO.input(ECHO[i]) == 0 and WDT_bln == False ):
                pulse_start = time.time()
                delta_time = time.time() - t_US_start
                if (delta_time >= SOUND_WAVE_TRAVEL):
                    WDT_bln = True
                
            while (GPIO.input(ECHO[i]) == 1 and WDT_bln == False):
                pulse_end = time.time()
                delta_time = time.time() - t_US_start
                if (delta_time >= SOUND_WAVE_TRAVEL):
                    WDT_bln = True
                
            
            # Calculate the travelled distance of the wave-sound
            if(WDT_bln == False):
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance, 2)
                Wave_Distance[i] = distance
                #print("Sensor{} : Distance {}cm".format(i, distance))
                delta_time = 0
            else:
                WDT_bln == False
                delta_time = 0
                Wave_Distance[i] = -1
                #print("Sensor{} -> WDT TimeOut".format(i))
                
            strDistance = strDistance + "," + str(distance)
                
        print("----------------------------------")
        t_end = time.time()
        print("Ultrasonic Sensor - Distance {} cm".format(Wave_Distance))
        
        print(strDistance)      # CSV format
        print("time spent {}".format(t_end - t_start))
        #time.sleep(0.2)
            
            
            
            
    GPIO.cleanup()


############################################################################################################################################
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
# main() Entry point
#-------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    
    main()
#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------

