import loop

playlist=["first.wav","second.wav","third.wav","fourth.wav"]
track=[]


for x in range(len(playlist)):
    track.append('')
    track[x]=loop.Looper(playlist[x])
    track[x].start()


        
def stopall():
    for x in range(len(track)):
        track[x].stop()
        
def playall():
    for x in range(len(track)):
        track[x].play()


if __name__ == '__main__':
    playall()


        
