#This imports us a SenseHat object 
from sense_emu import SenseHat
import time

#lets Define some vars
row = 8
bottom_row = 56
speed = 2

#RGB colors
white = (255, 255, 255)
blue  = (0, 0, 255)
reset = (0, 0, 0)

#This is our SenseHat object
sense = SenseHat()
#define some methods
def move(event):
    #move right
    if event.direction == "right":
        ourPixles[index] = reset
        ourPixles[index + 1] = white
    else:
        ourPixles[index] = reset
        ourPixles[index + 1] = white
#define what happens when the user presses left or right
sense.stick.direction_left = move
sense.stick.direction_right = move

#Clear out the sense hat
sense.clear()

#Has tetris scroll across the screen
sense.show_message("Tetris", 0.1 ,(255, 0, 0))

#Now get a list of pixles (Should be all blank)
ourPixles = sense.get_pixels()

#assign a starting pixle
ourPixles[3] = white
sense.set_pixels(ourPixles)

time.sleep(speed)

is_bottom = False
        
#keep repeting untill we reach the bottom
while is_bottom == False:
    #keep track of our position
    index = 0;
    #loop thru our list
    for x in ourPixles:
        if x == white:
            if index >= bottom_row:
                is_bottom = True
            else:
                #remove the top pixle and move it one below
                ourPixles[index] = reset
                ourPixles[index + row] = white
                sense.set_pixels(ourPixles)
                #this gives us a pause after each move
                time.sleep(speed)
        index += 1
print("Done")

