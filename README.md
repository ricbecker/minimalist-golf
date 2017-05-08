This is the GitHub repository for Night Multimedia Art’s “MINIMalist Golf” project.

There should be two main parts of this project: the audio engine and the battery / power control.

Required installations for this project:

Install pyaudio with command
sudo apt-get install python-pyaudio python3-pyaudio

if python.h not found, run:
sudo apt-get install python-dev python3-dev


The software will be divided into to two parts, the loop module and the signal module, with engine as the initialization / main control script.  currently engine initializes the playlist and readies for track[x].play(), pause(), and stop() commands.  the signal module will monitor sensor input and trigger the engine to play tracks; a timeout should call stopall() to end the session.


Helpful links:
http://www.voltaicsystems.com/blog/powering-a-raspberry-pi-from-solar-power/
https://www.buildxyz.xyz/raspberry-pi-shutdown-via-arduino/
http://raspberry.io/projects/view/reading-and-writing-from-gpio-ports-from-python/
