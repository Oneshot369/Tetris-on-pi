#This imports us a SenseHat object 
from sense_emu import SenseHat
import time

################################################
    #lets Define some vars
row = 8
speed = 2

#RGB colors
white = (255, 255, 255)
blue  = (0, 0, 255)
red  = (255, 0, 0)
reset = (0, 0, 0)

#This is our SenseHat object
sense = SenseHat()

#this is our 2 d array 64 lights
ourArr = [[0 for x in range(row)] for y in range(row)]

#######################################################
    #this section is for moving pixles (DOES NOT WORK CUS STUPID)
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
                
#moves the pixle down
def moveDown(x, y, ourArr):
    #checks if we would go out of bounds and does nothing if we would
    if x != row-1:
        ourArr[x][y] = reset
        ourArr[x + 1][y] = white

#moves the pixle left
def moveLeft(x, y, ourArr):
    #checks if we would go out of bounds and does nothing if we would
    if y != 0:
        ourArr[x][y] = reset
        ourArr[x][y-1] = white

#moves the pixle right
def moveRight(x, y, ourArr):
    #checks if we would go out of bounds and does nothing if we would
    if y != row-1:
        ourArr[x][y] = reset
        ourArr[x][y+1] = white

################################################
        #the following methods are for converting between 2d arr and list and setting a 2d Arr to the pixles

#converts a 2D Array to a list
def convertToList(ourArr):
    temList = []
    for x in range(row):
        for y in range(row):
            temList.append(ourArr[x][y])
    return temList

#converts a list into a 2d array
def convertTo2D(ourList):
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
    ourArr = convertTo2D(sense.get_pixels())
    return ourArr

#sets a 2D array into the sense hat
def setPixles(our2D):
    #covert our 2D to a list
    pixleList = convertToList(our2D)
    #set the list to pixles
    sense.set_pixels(pixleList)
    
##############################################
    
#function to do some things on startup
def start():
    #Clear out the sense hat
    sense.clear()

    #define what happens when the user presses left or right
    sense.stick.direction_left = move
    sense.stick.direction_right = move


    #Has tetris scroll across the screen
    sense.show_message("Tetris", 0.1 , blue)
    sense.clear()
    
#prints out our list of pixles
def printList(pixleList):
    for i in pixleList:
        print(i)
##############################################################
    # the 'main'

start()

#Now get a list of pixles (Should be all blank)
ourArr = convertTo2D(sense.get_pixels())

#assign a starting pixle
ourArr[0][3] = white
setPixles(ourArr)

time.sleep(speed)

is_bottom = False
        
#keep repeting untill we reach the bottom
while is_bottom == False:

    #loop thru our list
    for x in range(row):
        for y in range(row):
            #get our Array
            if ourArr[x][y] == white:
                if x >= row-1:
                    is_bottom = True
                else:
                    #remove the top pixle and move it one below
                    moveDown(x, y, ourArr)
                    setPixles(ourArr)
                    #this gives us a pause after each move
                    time.sleep(speed)

print("Done")

