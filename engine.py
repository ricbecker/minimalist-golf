import os
import loop
try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import sys
import threading
import pygame

pygame.init()

channel=[1,2,3,4]


def stopall():
    print(len(setup.track))
    for x in range(len(setup.track)):
        setup.track[x].stop()

def terminate():
    print("terminating")
    for x in range(len(setup.track)):
        try:
            setup.track[x].terminate()
            print("terminated",setup.track[x])
        except:
            pass

def timeout():
    print("play has timed out")
    try:
        pincancel()
    except:
        pass
    stopall()
#    trackset()
    try:
        pinset()
    except:
        pass
    print(threading.activeCount(),"alive")
            
def playall():
    for x in range(len(setup.track)):
        setup.track[x].play()
        
def detected(ballsack):
    print("sensor",ballsack," active")

    #clock settings
    
    try:
        detected.clock.cancel()
        print("clock cancelled")
    except:
        pass
    
    detected.clock=threading.Timer(39,timeout)
    detected.clock.start()

    #check track statuses and play
    
    if setup.playcounter==len(channel):
        setup.playcounter=0
        setup.roundcounter+=1;

    if setup.roundcounter==len(channel[0]):
        setup.roundcounter=0

    current=setup.track[setup.playcounter]
    print(current)
    filename=channel[setup.playcounter][setup.roundcounter]
    print(filename)
   
    if not setup.track[setup.playcounter].playing:
        current.replace(filename)
        time.sleep(.1)
        current.play()
    else:
        current.replace(filename)
    
    setup.playcounter +=1




def trackset():
    setup.track=[]
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
#        GPIO.add_event_detect(pinnum, GPIO.RISING, callback=detected, bouncetime=500)
        print("sensor ",pinnum," initalized")

def channelset(root):
    channel[0]=[root+"one.wav",root+"five.wav",root+"nine.wav"]
    print(channel[0])
    channel[1]=[root+"two.wav",root+"six.wav",root+"ten.wav"]
    channel[2]=[root+"three.wav",root+"seven.wav",root+"eleven.wav"]
    channel[3]=[root+"four.wav",root+"eight.wav",root+"twelve.wav"]
  


def setup():
    root="/home/pi/minimalist-golf"
    setup.track=[]
    setup.playcounter=0
    setup.roundcounter=0
    setup.numtracks=0

    try:
        GPIO.setmode(GPIO.BOARD)
        setup.senslist=[29,31,33,35]
        print(setup.senslist)
        print("pinmode established")
    except:
        print("no raspberry pi")
        root=""
        
    channelset(root)
    print("playlist initialized")
    trackset()

    sensor=[]

    try:
        pinset()
    except:
        pass
    count29=0
    count31=0
    count33=0
    count35=0
    try:
        while True:
            try:
                if(GPIO.input(29)==0 and count29==0):
                    print("read 29")
                    detected(29)
                    count29=1
                if(GPIO.input(29)==1 and count29==1):
                    count29=0
                if(GPIO.input(31)==0 and count31==0):
                    print("read 31")
                    detected(31)
                    count31=1
                if(GPIO.input(31)==1 and count31==1):
                    count31=0
                if(GPIO.input(33)==0 and count33==0):
                    print("read 33")
                    detected(33)
                    count33=1
                if(GPIO.input(33)==1 and count33==1):
                    count33=0
                if(GPIO.input(35)==0 and count35==0):
                    print("read 35")
                    detected(35)
                    count35=1
                if(GPIO.input(35)==1 and count35==1):
                    count35=0
            except:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w]:
                    print("keyboard input received")
                    detected("keyboard")
                pygame.event.pump()
                
            time.sleep(.1)
            
    except KeyboardInterrupt:
        terminate()
        time.sleep(1)
        print ("Quit")
        GPIO.cleanup()
        os._exit(0)
        


if __name__ == '__main__':
    setup()
    


        
