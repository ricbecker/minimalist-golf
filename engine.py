import loop
import RPi.GPIO as GPIO
import time
import threading


channel=[1,2,3,4]


def stopall():
    for x in range(4):
        setup.track[x].stop()

def terminate():
    for x in range(len(setup.track)):
        setup.track[x].terminate()

            
def playall():
    for x in range(len(setup.track)):
        setup.track[x].play()
        
def detected(ballsack):
    print("sensor active")
    try:
        detected.clock.cancel()
    except:
        pass
    detected.clock=threading.Timer(30,timeout)
    detected.clock.start()
    if setup.playcounter==len(channel):
        setup.playcounter=0
        setup.roundcounter+=1;

    if setup.roundcounter==len(channel[0]):
        setup.roundcounter=0

    if not setup.track[setup.playcounter].playing:
        setup.track[setup.playcounter].play()
    else:
        filename=channel[setup.playcounter][setup.roundcounter]
        print(filename)
        setup.track[setup.playcounter].replace(filename)
    setup.playcounter +=1

def timeout():
    print("play has timed out")
    setup.playcounter=0
    setup.roundcounter=0
    stopall()
    time.sleep(.2)
    trackset()

def trackset():
    for x in range(len(channel)):
        setup.track.append('')
        setup.track[x]=loop.Looper(channel[x][0])
        setup.track[x].start()
        setup.numtracks+=1


def setup():
    channel[0]=["/home/pi/minimalist-golf/one.wav","/home/pi/minimalist-golf/five.wav"]
    channel[1]=["/home/pi/minimalist-golf/two.wav","/home/pi/minimalist-golf/six.wav"]
    channel[2]=["/home/pi/minimalist-golf/three.wav","/home/pi/minimalist-golf/seven.wav"]
    channel[3]=["/home/pi/minimalist-golf/four.wav","/home/pi/minimalist-golf/eight.wav"]
    setup.track=[]
    setup.playcounter=0
    setup.roundcounter=0
    setup.numtracks=0

    trackset()

    print("playlist initialized")
    pinnum=0
    print(pinnum)
    GPIO.setmode(GPIO.BOARD)
    setup.senslist=[33]
    print(setup.senslist)
    print("pinmode established")

    sensor=[]

    for x in range(len(setup.senslist)):
        pinnum=setup.senslist[x]
        GPIO.setup(pinnum,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pinnum, GPIO.RISING, callback=detected, bouncetime=500)
        print("sensor ",pinnum," initalized")

    try:
        while True:
            pass
            time.sleep(.1)
    except KeyboardInterrupt:
        terminate()
        time.sleep(1)
        print ("Quit")
        GPIO.cleanup()

        


if __name__ == '__main__':
    setup()
    


        
