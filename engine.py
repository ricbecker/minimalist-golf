import loop
#import breakbeam
import RPi.GPIO as GPIO
import time
import threading



def stopall():
    for x in range(len(setup.track)):
        setup.track[x].stop()
def terminate():
    for x in range(len(setup.track)):
        setup.track[x].terminate()

            
def playall():
    for x in range(len(setup.track)):
        setup.track[x].play()
        
def detected(channel):
    print("Pin ",channel," triggered")
    tracknum=setup.senslist.index(channel)
    print("Sensor",tracknum," active")
    print("Playcount is ", setup.playcounter)
    setup.track[setup.playcounter].play()
    setup.playcounter +=1
    if setup.playcounter > 3:
        setup.playcounter=0
        print("playcount reset")
    else:
        print("playcount incremented")


def setup():
    playlist=["first.wav","second.wav","third.wav","fourth.wav"]
    setup.track=[]
    setup.playcounter=0

    print("setup playlist")

    for x in range(len(playlist)):
        setup.track.append('')
        setup.track[x]=loop.Looper(playlist[x])
        setup.track[x].start()
    print("playlist initialized")
    print("set up pinmode")
    pinnum=0
    print(pinnum)
    GPIO.setmode(GPIO.BOARD)
    setup.senslist=[11,12,35]
    print(setup.senslist)
    print("pinmode established")

    print("set up pins")

    sensor=[]

    for x in range(len(setup.senslist)):
        pinnum=setup.senslist[x]
        GPIO.setup(pinnum,GPIO.IN)
        GPIO.add_event_detect(pinnum, GPIO.RISING, callback=detected, bouncetime=10000)
        print("sensor ",pinnum," initalized")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        terminate()
        time.sleep(2)
        print ("Quit")
        GPIO.cleanup()

        


if __name__ == '__main__':
    setup()
    


        
