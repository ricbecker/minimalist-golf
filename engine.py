import loop
import breakbeam

def setup():
    playlist=["first.wav","second.wav","third.wav","fourth.wav"]
    track=[]


    for x in range(len(playlist)):
        track.append('')
        track[x]=loop.Looper(playlist[x])
        track[x].start()

    senslist=[11,12,35]
    sensor=[]

    for x in range(len(playlist)):
        sensor.append('')
        sensor[x]=breakbeam.Detect(sensor[x])



def stopall():
    for x in range(len(track)):
        track[x].stop()
            
def playall():
    for x in range(len(track)):
        track[x].play()


if __name__ == '__main__':
    setup()
    


        
