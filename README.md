This is the GitHub repository for Night Multimedia Art’s “MINIMalist Golf” project.

There should be two main parts of this project: the audio engine and the battery / power control.

Required installations for this project:

Install pyaudio with command
sudo apt-get install python-pyaudio python3-pyaudio

if python.h not found, run:
sudo apt-get install python-dev python3-dev


The Audio Engine will be divided into to two parts, the loop module and the signal module. The loop is a threaded module and will use pyaudio to play, pause, or stop 4 audio tracks calling on filenames first.wav, second.wav, third.wav, fourth.wav and the signal module will communicate with the ADC attached to the RPi and play tracks by calling a thread for each track and a command to play.  Initialization of the program will start() all threads and termination of the program will stop all tracks playing, but the thread will continue. for example initialization will call track1.start() to start the thread without playing audio, then on receiving a signal from the sensor the signal module will call track1.play() and on timeout will call track1.stop()

Loop.py
  Class Looper(filename)
  
Signal receiver (not yet created)
  

