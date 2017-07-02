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
