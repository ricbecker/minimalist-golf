import os
import loop
try:
    import RPi.GPIO as GPIO
    root="/home/pi/minimalist-golf/"
    pimode=True
except:
    pimode=False
    root=""
        
import time
import sys
import threading
import pygame
from datetime import datetime as thetime
import logging

logging.basicConfig(level=logging.DEBUG, filename='enginelog')
pygame.init()
channel=[1,2,3,4]
_log=""
clock=False


def stopall():
    for x in range(len(setup.track)):
        setup.track[x].stop()

def terminate():
    for x in range(len(setup.track)):
        try:
            setup.track[x].terminate()
        except:
            pass

def timeout():
    global clock
    clock=False
    log("play has timed out")
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
            
def playall():
    for x in range(len(setup.track)):
        setup.track[x].play()
        
def detected(sensor):
    global clock
    


    #clock settings

    if clock==False:
        log("newclock")
        
    try:
        clock.cancel()
    except:
        pass
    
    log("Sensor "+str(sensor)+" active")
    
    clock=threading.Timer(3,timeout)
    clock.start()

    #check track statuses and play
    
    if setup.playcounter==len(channel):
        setup.playcounter=0
        setup.roundcounter+=1;

    if setup.roundcounter==len(channel[0]):
        setup.roundcounter=0

    current=setup.track[setup.playcounter]
    filename=channel[setup.playcounter][setup.roundcounter]
   
    if not setup.track[setup.playcounter].playing:
        current.replace(filename)
        current.play()
    else:
        current.replace(filename)
    
    setup.playcounter +=1

    log("Program advanced")
    time.sleep(1)




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
        log("sensor ",pinnum," cancelled")


def pinset():
    log("running pinset")
    for x in range(len(setup.senslist)):
        pinnum=setup.senslist[x]
        GPIO.setup(pinnum,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#        GPIO.add_event_detect(pinnum, GPIO.RISING, callback=detected, bouncetime=500)
        log("sensor "+str(pinnum)+" initalized")

def channelset():
    global root
    channel[0]=[root+"one.wav",root+"five.wav",root+"nine.wav"]
    channel[1]=[root+"two.wav",root+"six.wav",root+"ten.wav"]
    channel[2]=[root+"three.wav",root+"seven.wav",root+"eleven.wav"]
    channel[3]=[root+"four.wav",root+"eight.wav",root+"twelve.wav"]
  
def log(entry):
      global _log
      global root
      appender=""
      if(entry=="newclock"):
         appender="""\n
           ||############## NEW CLOCK ##################||\n
           ||###########################################||\n
                     \n"""
      if(entry=="newprogram"):
         appender="""\n\n\n\n
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
      %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%
    %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%  %%

\n
\n
           ||@@@@@@@@@@@@@ NEW PROGRAM @@@@@@@@@@@@@@@@@||\n
           ||@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||\n
\n
\n"""
      appender+=str(thetime.now())+": "+entry+"\n"
      print(appender)
      f=open(root+"enginelog", "a+")
      f.write(appender)
      f.close()
      

def setup():
    global root
    global clock

    try:
        GPIO.setmode(GPIO.BOARD)
        setup.senslist=[29,31,33,35]
    except:
        pass
        

    
    setup.track=[]
    setup.playcounter=0
    setup.roundcounter=0
    setup.numtracks=0


        
    channelset()
    log("playlist initialized")
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
            if(pimode==True):
                if(GPIO.input(29)==0 and count29==0):
                    log("read 29")
                    detected(29)
                    count29=1
                if(GPIO.input(29)==1 and count29==1):
                    count29=0
                if(GPIO.input(31)==0 and count31==0):
                    log("read 31")
                    detected(31)
                    count31=1
                if(GPIO.input(31)==1 and count31==1):
                    count31=0
                if(GPIO.input(33)==0 and count33==0):
                    log("read 33")
                    detected(33)
                    count33=1
                if(GPIO.input(33)==1 and count33==1):
                    count33=0
                if(GPIO.input(35)==0 and count35==0):
                    log("read 35")
                    detected(35)
                    count35=1
                if(GPIO.input(35)==1 and count35==1):
                    count35=0

            try:
                pygame.init()
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w]:
                    detected("keyboard")
                if pressed[pygame.K_q]:
                    try:
                        clock.cancel()
                    except:
                        pass
                    if clock:
                        timeout()
                pygame.event.pump()
            except:
                pass    
            time.sleep(.01)
            
    except KeyboardInterrupt:
        terminate()
        time.sleep(1)
        log("Quit by user")
        try:
            GPIO.cleanup()
        except:
            pass
        os._exit(0)


        


if __name__ == '__main__':
    log("newprogram")
    if pimode:
        log("Pi Mode Engaged")
    else:
        log("NoPi Mode Engaged")
        
    try:
        setup()
    except:
        logging.exception("oops")
        

        

    


        
