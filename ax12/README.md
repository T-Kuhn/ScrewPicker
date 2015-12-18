###AX-12 Python Library (for RaspberryPi)

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/

Use it at your own risk. Assume that I have no idea what I am doing.

This is a more object-oriented version of [Jesse Merritt's script](https://github.com/jes1510/python_dynamixels) to control AX-12 servos using a Raspberry Pi.

Based on [original script by Inxfergy](http://forums.trossenrobotics.com/tutorials/how-to-diy-128/controlling-ax-12-servos-3275/),
and heavily inspired by the [Arduino AX-12 library](http://savageelectronics.blogspot.it/2011/01/arduino-y-dynamixel-ax-12.html) by
Josué Alejandro Savage.

The script assumes that the Raspberry Pi  is connected to the servos through
a buffer such as a 74HC241. The communication direction is controlled through
GPIO pin 18, and Serial communication Rx and Tx through GPIO pins 15 and 14,
respectivelly.

A schematic for the circuit can be found on page 8 of the [AX-12 manual](http://www.trossenrobotics.com/images/productdownloads/AX-12%28English%29.pdf).

The startup config of the Raspberry Pi has to be modified to set the UART
clock to allow for 1Mbps baud. The TTY attached to the COM port has to be
disabled, and the baud rate of the TTY has to be set to 1Mbps.

From [Oppedijk](http://www.oppedijk.com/robotics/control-dynamixel-with-raspberrypi):

Add the following line to /boot/config.txt:  
init_uart_clock=16000000  
  
Edit /boot/cmdline.txt and remove all options mentioning ttyAMA0.  
Edit /etc/inittab and comment out any lines mentioning ttyAMA0.  
  
Add the following line to ~/.bashrc:  
sudo stty -F /dev/ttyAMA0 1000000  

###Dependencies:  
- [pySerial](http://pyserial.sourceforge.net/)  
- [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)  
