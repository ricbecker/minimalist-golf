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
    detected.clock=threading.Timer(20,timeout)
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
    pincancel()
    setup.playcounter=0
#    setup.roundcounter=0
    stopall()
    time.sleep(.2)
    trackset()
    pinset()

def trackset():
    for x in range(len(channel)):
        setup.track.append('')
        setup.track[x]=loop.Looper(channel[x][setup.roundcounter])
        setup.track[x].start()
        setup.numtracks+=1

def pincancel():

    for x in range(len(setup.senslist)):
        pinnum=setup.senslist[x]
        GPIO.remove_event_detect(pinnum)
        print("sensor ",pinnum," cancelled")


def pinset():

    for x in range(len(setup.senslist)):
        pinnum=setup.senslist[x]
        GPIO.setup(pinnum,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pinnum, GPIO.RISING, callback=detected, bouncetime=500)
        print("sensor ",pinnum," initalized")


def setup():
    channel[0]=["/home/pi/minimalist-golf/one.wav","/home/pi/minimalist-golf/five.wav","/home/pi/minimalist-golf/nine.wav"]
    channel[1]=["/home/pi/minimalist-golf/two.wav","/home/pi/minimalist-golf/six.wav","/home/pi/minimalist-golf/ten.wav"]
    channel[2]=["/home/pi/minimalist-golf/three.wav","/home/pi/minimalist-golf/seven.wav","/home/pi/minimalist-golf/eleven.wav"]
    channel[3]=["/home/pi/minimalist-golf/four.wav","/home/pi/minimalist-golf/eight.wav","/home/pi/minimalist-golf/twelve.wav"]
    setup.track=[]
    setup.playcounter=0
    setup.roundcounter=0
    setup.numtracks=0

    trackset()

    print("playlist initialized")
    GPIO.setmode(GPIO.BOARD)
    setup.senslist=[29,31,33,35]
    print(setup.senslist)
    print("pinmode established")

    sensor=[]

    pinset()

    try:
        while True:
            pass
            time.sleep(.5)
    except KeyboardInterrupt:
        terminate()
        time.sleep(1)
        print ("Quit")
        GPIO.cleanup()

        


if __name__ == '__main__':
    setup()
    


        
