<<<<<<< HEAD
import RPi.GPIO as GPIO
import os
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pin=32

GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
    while True:
        print("waiting")
        GPIO.wait_for_edge(pin, GPIO.RISING)
        print("button pressed")
        sleep(2)
        if GPIO.input(pin)==1:
            print("shutting down")
            os.system("sudo shutdown -h now")

if __name__ == '__main__':
        main()
=======
import os
import time
from datetime import datetime as thetime
import RPi.GPIO as GPIO

def shutdown(pinnum):
    print("button")
    time.sleep(3)
    if(GPIO.input(32)==1):
        print("still pressed")
        os.system("sudo shutdown -h now")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(32, GPIO.RISING, callback=shutdown)

if __name__=='__main__':
    while True:
        time.sleep(1)
>>>>>>> e13d051539109c16cb3e1925f7b734256d484110
