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
        -- loop (boolean)    : True if you want loop playback. 
                               False otherwise.
    """
    print("intialize class")
    super(Looper, self).__init__()
    time.sleep(1)
    print("set filepath")
    self.filepath = os.path.abspath(filepath)
    self.loop = loop
    self.playing = False
    self.pauser = False

  def run(self):
    print("running run function")
    # Open Wave File and start play!
    self.wf = wave.open(self.filepath, 'rb')
    player = pyaudio.PyAudio()



    # Open Output Stream (basen on PyAudio tutorial)
    stream = player.open(format = player.get_format_from_width(self.wf.getsampwidth()),
        channels = self.wf.getnchannels(),
        rate = self.wf.getframerate(),
        output = True)

    # PLAYBACK LOOP
    data = self.wf.readframes(self.CHUNK)
    while self.loop :
      if self.playing:
        stream.write(data)
        data = self.wf.readframes(self.CHUNK)
      if self.loop and not data:
        self.wf.rewind()
        data = self.wf.readframes(self.CHUNK)

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

