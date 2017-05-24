This is the GitHub repository for Night Multimedia Art’s “MINIMalist Golf” project.
______________

Required installations for this project:

Install pyaudio with command
sudo apt-get install python-pyaudio python3-pyaudio

if python.h not found, run:
sudo apt-get install python-dev python3-dev
_______________

There are two programs running on the Pi: the main engine (includes the Loop module, a separate file) and the power control (a simple background process that reads for GPIO signals to shutdown the pi). There is additional software installed on an arduino to read the battery state and a clock and send signals to the Pi to shutdown.
_______________

Method for running a script on Pi startup:

-from terminal, open crontab with command 
        crontab -e
-At bottom of crontab file, insert command:
        @reboot python <full file path of python file> &
-save and exit. voila!

NB: "&" is essential for a script which contains an infinite loop so that the computer continues booting after loading.

____________________________

PINS:
- ARDUINO
        - digital pin 10 - output - shutdown signal to raspberry pi
        - digital pin 12 - output - signal to power relay
- RASPBERRY PI
        - digital pin 19 - input - shutdown signal from arduino

____________________________

Helpful links:
http://www.voltaicsystems.com/blog/powering-a-raspberry-pi-from-solar-power/
https://www.buildxyz.xyz/raspberry-pi-shutdown-via-arduino/
http://raspberry.io/projects/view/reading-and-writing-from-gpio-ports-from-python/
