import RPi.GPIO as GPIO
import time
import threading

class Detect(threading.Thread):
    def __init__(self,PIR_PIN):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIR_PIN,GPIO.IN)

    try:
        print "PIR Module Test (CTRL+C to exit)"
        time.sleep(2)
        print "Ready"
        while True:
            if GPIO.input(PIR_PIN):
                print "Motion Detekalected beyotch"
            time.sleep(1)
    except KeyboardInterrupt:
        print "Quit"
        GPIO.cleanup()
