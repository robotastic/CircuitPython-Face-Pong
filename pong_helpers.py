from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
import usefulsensors_persondetector
import math


class AutoBall:
    def __init__(self, diameter, start_x, start_y, screen_width, screen_height, debug=False):
        # Store local variables in our object to access later in other functions
        self.diameter = diameter
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y

        # Create a circle object for the screen
        self.circle = Circle(self.x, self.y, self.diameter, fill=0xFF0000)

        # default to moving right
        self.going_down = True

        # up/down movement amount. Default to horizontal only
        self.x_offset = 0

        # Need screen height and width to check for collision with top/bottom and both side edges
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width


    # function to check for collisions between this ball
    # and the left and right paddle objects that get passed in as parameters
    def check_collisions(self, top_paddle, bottom_paddle):
        #TODO: figure out if the x/y coordinate of the ball is centered or top left and adjust the collision check accordingly.

        if self.y <= top_paddle.y + top_paddle.height and top_paddle.x < self.x < top_paddle.x + top_paddle.width:
            # if we collide with top paddle then check if the paddle was in motion, if so adjust the x_offset.
            if top_paddle.prev_x > top_paddle.x:
                #print("left paddle moving down")

                # paddle is moving right on screen
                if self.x_offset > -1:
                    self.x_offset += 1

            elif top_paddle.prev_x < top_paddle.x:
                #print("left paddle moving up")

                # paddle is moving left on screen
                if self.x_offset < -1:
                    self.x_offset -= 1

            #change direction to move right
            self.going_down = True



        if self.y >= bottom_paddle.y - bottom_paddle.height and bottom_paddle.x < self.x < bottom_paddle.x + bottom_paddle.width:
            # if we collide with right paddle then then check if the paddle was in motion, if so adjust the y_offset.

            if bottom_paddle.prev_x > bottom_paddle.x:
                # paddle is moving down on screen
                if self.x_offset > -1:
                    self.x_offset -= 1

            elif bottom_paddle.prev_x < bottom_paddle.x:
                # paddle is moving up on screen
                if self.x_offset < 1:
                    self.x_offset += 1

            #change direction to move left
            self.going_down = False



    # you must call update() from inside of main loop and pass the paddle objects
    def update(self, top_paddle, bottom_paddle):

        # check which horizontal direction we are moving and adjust x coordinate accordingly.
        if self.going_down == True:
            self.y += 1
        else:
            self.y -= 1

        # move in y direction by y_offset. This makes the ball move diagonal if y_offset is not 0.
        self.x += self.x_offset


        # check if ball went off top edge
        if self.y < 0:
            # reset back to center
            self.x = self.start_x
            self.y = self.start_y

        # check if ball went off bottom edge
        if self.y > self.SCREEN_HEIGHT - self.diameter:
            # reset back to center
            self.x = self.start_x
            self.y = self.start_y

        # if we are at the left wall
        if self.x == 0:
            # flip y_offset to opposite side of 0 to change direction
            self.x_offset = self.x_offset * -1

        # if we are at the right wall
        if self.x == self.SCREEN_WIDTH - (self.diameter+1)*2:
            # flip y_offset to opposite side of 0 to change direction
            self.x_offset = self.x_offset * -1

        # check for collisions with paddles
        self.check_collisions(top_paddle, bottom_paddle)

        # copy over x and y coordinates to the circle object so it takes effect on the screen
        self.circle.x = self.x
        self.circle.y = self.y


"""
Pong paddle controlled manually by two buttons specified as strings passed into the constructor.
"""
class SensorPaddle:
    def __init__(self, width, height, start_x, start_y, screen_width, screen_height, i2c, debug=False):

        self.sensor = usefulsensors_persondetector.PersonDetector(i2c)
        #self.sensor.setIdModelEnabled(False)
        #self.sensor.setPersistentIds(False)
        # Store local variables in our object to access later in other functions
        self.height = height
        self.width = width
        self.x = start_x
        self.y = start_y

        # will store previous update y position to determine if paddle is in motion
        self.prev_y = self.y

        # create a rect object
        self.rect = Rect(self.x, self.y, self.width, self.height, fill=0xffffff)


        # screen height needed so it knows when to stop moving
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width


    # You must call update() from inside the main loop of code.py
    def update(self):
        #(x0,y0,x1,y1,confidence,id,id_confidence) = self.sensor.read()
        results = self.sensor.read()
        num_faces = results[0]
        bboxes = results[1]
        best_bbox = None
        best_confidence = 0

        for i in range(num_faces):
            bbox = bboxes[i]
            if bbox["confidence"] > best_confidence:
                best_bbox = bbox 
            #print("X0: ",bbox["x0"]," Y0: ",bbox["y0"]," X1: ", bbox["x1"]," Y1: ", bbox["y1"], " Confidence: ", bbox["confidence"], " ID: ", bbox["id"], " ID Confidence: ", bbox["id_confidence"], " Face On: ", bbox["face_on"] )

        if best_bbox:
            self.prev_x = self.x
            x_max = 255
            middle_x = ((best_bbox["x1"]-best_bbox["x0"]) / 2) + best_bbox["x0"]
            x = middle_x - (x_max/2)
            x = x * 3
            if x > (x_max/2): x = (x_max/2)
            if x < -(x_max/2): x = -(x_max/2)

            x = x + (x_max/2)

            x = (x/x_max) * self.SCREEN_WIDTH
            x = self.SCREEN_WIDTH -  int(x)

            if x > (self.SCREEN_WIDTH-self.width-1): x = self.SCREEN_WIDTH-self.width-1

            if x < 0: x = 0

            self.x = x
            # copy over x and y from local vars into the rect so it takes effect on the screen
            self.rect.x = self.x
            self.rect.y = self.y


"""
Pong paddle object that moves up and down on it's own, tries to follow the ball.
"""
class AutoPaddle:
    def __init__(self, width, height, start_x, start_y, screen_width, screen_height, debug=False):
        # Store local variables in our object to access later in other functions
        self.height = height
        self.width = width
        self.x = start_x
        self.y = start_y

        # will store previous update y position to determine if paddle is in motion
        self.prev_y = self.y

        # create a rect object
        self.rect = Rect(self.x, self.y, self.width, self.height, fill=0xffffff)

        # default to moving up
        self.going_up = True

        # screen height needed so it knows when to change direction
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_WIDTH = screen_width

    # You must call update() from inside the main loop of code.py
    def update(self, ball):
        #print("inside paddle update")
        self.prev_x = self.x

        # check if the ball is higher or lower than us and move accordingly
        if self.x + self.width/2 > ball.x and self.x > 0:
            self.x -= 1
        elif self.x + self.width/2 < ball.x and self.x < self.SCREEN_WIDTH - self.width:
            self.x += 1


        # copy over x and y from local vars into the rect so it takes effect on the screen
        self.rect.x = self.x
        self.rect.y = self.y