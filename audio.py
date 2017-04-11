import pyaudio
import wave
import sys

CHUNK = 1024

forplay=("/Users/ricbecker/Music/yearning.wav")
forplay2=("/Users/ricbecker/Music/wozzeck.wav")

wf = wave.open(forplay, 'rb')
wf2 = wave.open(forplay2, 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
