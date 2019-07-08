A copy of the [http://lightshowpi.org/](http://lightshowpi.org/) project (version 1.4) with some additional bits to make a Peugot 208 Instrument cluster dance.



Hardware required is:
Pi 3 Model B
CAN adaptor, must be recognised as a SocketCAN interface
Speaker, plugged in to the Pi

To install - clone this Repo and then run the installer
cd /home/pi/lightshowpi
sudo ./install.sh

Now reboot the Pi

Two files have been modified from the original LightShowPi project.

1. /py/cansend.py - this is the main file where all of the CAN work is done.
2. /py/synchronized_lights.py - this is the original project file that has been changed to feed data into cansend.py

To get working - ensure a CAN interface is set up and mapped to CAN0, use "candump can0" to test. The speed of this interface must be set at up time, it's not set in the code.

Now run lightshow Pi giving it a file, it'll play the music and soon after drive the clocks

sudo python py/synchronized_lights.py --file=/home/pi/Desktop/Dual_Core_-_All_The_Things_Official-FoUWHfh733Y\ \(1\).mp3


If you get errors, make sure the CAN interface is up and running ok

sudo ip link set can0 type can bitrate 125000
sudo ip link set up can0
