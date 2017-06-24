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
