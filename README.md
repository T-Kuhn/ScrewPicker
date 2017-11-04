# ScrewPicker

A Raspberry Pi project for a small robotic arm capable of picking up screws and other metallic things.

[https://youtu.be/bL8fScdBOos](https://youtu.be/bL8fScdBOos)

Important parts of the robot arm:

- 4 Dynamixel AX-12A servos
- Raspberry Pi camera module
- a small circuit for the communication Raspberry Pi - servos

The code can be broken down in to three junks. The first junk has servoHandler.py as it's main file. it uses [this](https://github.com/thiagohersan/memememe/tree/master/Python/ax12) ax12 library
to communicate with the servo motors. The next junk of code processes the image data. It's all about image processing (see ImPro.py, PixelObj.py).
And lastly, there's screwPicker.py, which is the main python-file. it should be executed to start the robot arm.

```engine='sh'
$ sudo python screwPicker.py
```

[Blog post](http://electrondust.com/2017/10/28/raspberry-pi-robot-arm-with-simple-computer-vision/) about the project.
