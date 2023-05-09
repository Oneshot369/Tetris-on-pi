#This imports us a SenseHat object 
from sense_emu import SenseHat
import time

################################################
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

#this is our 2 d array 64 lights
ourArr = [[0 for x in range(row)] for y in range(row)]

#######################################################
    #define some methods
#move mothod - this does not work yet
def move(event):
    print("move method")
    #get our list
    ourPixles = sense.get_pixels()
    printList(ourPixles)
    for x in ourPixles:
        if x == white:
            #move right
            if event.direction == "right":
                print("moving right")
                ourPixles[x] = reset
                ourPixles[x + 1] = white
            else:
                print("moving left")
                ourPixles[x] = reset
                ourPixles[x - 1] = white

#prints out our list of pixles
def printList(pixleList):
    for i in pixleList:
        print(i)
#converts a list into a 2d array
def convert2D(ourList):
    #vars
    x, y = 0, 0
    temArr = [[0 for x in range(row)] for y in range(row)]
    
    #loop thru our list
    for i in ourList:
        #copy each index from our list into temArr
        temArr[x][y] = i
        y += 1
        
        #one we reach the end of our row, set x back to zero and increase y by 1
        if y == row:
            y = 0
            x += 1
            
    #return our array
    return temArr
# gets a list from the sense hat and converts to a 2darray
def getArr():
    x = 1
##############################################################
    # the 'main'
#Clear out the sense hat
sense.clear()

ourArr = convert2D(sense.get_pixels())
printList(ourArr)

#define what happens when the user presses left or right
sense.stick.direction_left = move
sense.stick.direction_right = move


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

