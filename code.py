import board
import busio
import displayio
import framebufferio
from adafruit_display_shapes.circle import Circle
import time
from pong_helpers import SensorPaddle, AutoBall, AutoPaddle


import rgbmatrix
displayio.release_displays()


matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=6,
    rgb_pins=[board.R0, board.G0, board.B0, board.R1, board.G1, board.B1],
    addr_pins=[board.ROW_A, board.ROW_B, board.ROW_C, board.ROW_D, board.ROW_E],
    clock_pin=board.CLK, latch_pin=board.LAT, output_enable_pin=board.OE)

i2c_bus = busio.I2C(board.SCL, board.SDA)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
# width and height variables used to check the edges
SCREEN_WIDTH = display.width
SCREEN_HEIGHT = display.height

# FPS setting raise or lower this to make the game faster or slower
FPS = 60

# what fraction of a second to wait in order to achieve FPS setting
FPS_DELAY = 1 / FPS



# Make the display context
splash = displayio.Group()

# Make a background color fill
color_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
splash.append(bg_sprite)

# hold the time we last updated the game state
last_update_time = 0

# create left paddle
# up_btn = select, down_btn = down
#(self, width, height, start_x, start_y, screen_height, i2c, debug=False):
top_paddle = AutoPaddle(15,2,1,0,  SCREEN_WIDTH, SCREEN_HEIGHT)
bottom_paddle = SensorPaddle(15,2,SCREEN_WIDTH-15-3,SCREEN_HEIGHT-3, SCREEN_WIDTH,SCREEN_HEIGHT, i2c_bus)

# add it to screen group
splash.append(top_paddle.rect)

# create right paddle
# up_btn = start, down_btn = b


# add it to screen group
splash.append(bottom_paddle.rect)

# create ball
ball = AutoBall(1, int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), SCREEN_WIDTH, SCREEN_HEIGHT)

# add it to screen group
splash.append(ball.circle)
display.show(splash)
# variable to hold current time
now = 0

# debug variable to count loops inbetween updates
loops_since_update = 0

# update() function will get called from main loop
# hopefully at correct speed to match FPS setting
def update():
    #print("inside update

    # call update on all objects
    top_paddle.update(ball)
    bottom_paddle.update()
    ball.update(top_paddle, bottom_paddle)

while not i2c_bus.try_lock():
    pass

try:
    while True:
        # update time variable
        now = time.monotonic()

        # check if the delay time has passed since the last game update
        if last_update_time + FPS_DELAY <= now:
            #print("%s - %s" % ((last_loop_time + FPS_DELAY), now))

            # call update
            update()

            # set the last update time to now
            last_update_time = now

            #print(loops_since_update)
            # reset debug loop counter
            loops_since_update = 0
            
        else:
            # update debug loop counter
            loops_since_update += 1
            display.refresh()

except Exception as e: print(e)
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c_bus.unlock()