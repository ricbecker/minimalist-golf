import os
import wave
import threading
import sys
import time

# PyAudio Library
import pyaudio

class Looper(threading.Thread) :
  """
  A simple class based on PyAudio to play wave loop.
  It's a threading class. You can play audio while your application
  continues to do its stuff. :)
  """

  CHUNK = 1024


  def __init__(self,filepath,loop=True) :
    """
    Initialize `Looper` class.
    PARAM:
        -- filepath (String) : File Path to wave file.
        -- loop (booleanpy)    : True if you want loop playback. 
                               False otherwise.
    """
    print("intialize class, sleep .1 second")
    super(Looper, self).__init__()
    time.sleep(.1)
    print("set filepath")
    self.filepath = os.path.abspath(filepath)
    self.loop = True
    self.playing = False

  def run(self):
    # Open Wave File and start play!
    self.wf = wave.open(self.filepath, 'rb')
    self.numframes = self.wf.getnframes()
#    CHUNK=self.numframes
#    print(CHUNK)
    player = pyaudio.PyAudio()


    # Open Output Stream (basen on PyAudio tutorial)
    stream = player.open(format = player.get_format_from_width(self.wf.getsampwidth()),
        channels = self.wf.getnchannels(),
        rate = self.wf.getframerate(),
        output = True)
    print("intializing audio track sleep 1s")
    time.sleep(.1)

    # PLAYBACK LOOP
    self.data = self.wf.readframes(self.CHUNK)
    while self.loop :
      if self.playing:
        stream.write(self.data)
        self.data = self.wf.readframes(self.CHUNK)
      if self.loop and not self.data:
        self.wf.rewind()
        self.data = self.wf.readframes(self.CHUNK)
      time.sleep(.001)
    stream.close()
    player.terminate()


  def play(self) :
    """
    Just another name for self.start()
    """
    self.playing = True
    self.loop = True

  def pause(self) :
    if self.playing:
        self.playing=False
    else:
        self.playing=True


  def stop(self) :
      self.playing = False

  def terminate(self) :
    self.loop=False

  def replace(self,filename):
    self.wf = wave.open(filename, 'rb')

  def rewind()
    self.wf.rewind()

