# CircuitPython Face Pong

**This is a simple game of Pong... that you play with your face!** 

It uses the Useful Sensors Person Detector to find your face and you move back in forth in front of the camera to move to paddle and try to beat the computer.

The game extends the FoamyGuy's CircuitPython [pong game](https://github.com/FoamyGuy/CircuitPython-Badge-One-Player-Pong) to make it work on an RGB Matrix and work with the Person Detector.

### Required Libraries
- [Useful Sensors Person Detector Driver](https://github.com/robotastic/CircuitPython_UsefulSensors_PersonDetector)
- rgbmatrix
- adafruit_display_shapes
- board
- busio
- displayio
- framebufferio

### Hardware

It has been tested using:
- [64x64 RGB LED Matrix - 3mm Pitch](https://www.adafruit.com/product/4732)
- [Interstate 75 - RGB LED Matrix Driver](https://shop.pimoroni.com/products/interstate-75?variant=39443584417875)

The Interstate 75 is a nice little RGB Driver board from Pimoroni and it is built around the Raspberry PI RP2040 MCU. It can support Arduino and Circuit Python, and has a Stemma QT/Qwiic port built in. To add the sensor, you just have to plug it in.

This should also work with Adafruit's [Matrix Portal](https://www.adafruit.com/product/4745).

The game is broken into two files: 

 - code.py - Contains the main loop, RGB Matrix setup, and manages high-level game object update function calls.
 - pong_helpsers.py - contains helper objects for the game elements. code.py imports, creates, and calls update() on these objects at the appropriate time. The update() functions that are defined in this file control the behavior of the three types of game elements, sensor paddles, auto paddles, and balls. The bottom in this variant of the game is controlled by the data from the sensor. The top paddle is controlled automatically by an algorithm in the update() function. It tries to keep it's center aligned vertically with the ball. The ball moves automatically and changes direction when it collides with a paddle.
 

## Extend it further

This is a basic game, there is a lot that can be done it extend it further. Fork this game and make it awesome!
- Add some score keeping
- Improve the calculations for the angle of the ball bouncing off the paddles
- Turn it into Breakout!
