#This imports us a SenseHat object 
from sense_emu import SenseHat
import time
import threading

################################################
    #lets Define some vars
row = 8
speed = 1

#RGB colors
white = (255, 255, 255)
blue  = (0, 0, 255)
red  = (255, 0, 0)
green = (0, 255, 0)
reset = (0, 0, 0)

#This is our SenseHat object
sense = SenseHat()

#x and y of our block
xBlock = 0
yBlock = 0

#a mutex
lock = threading.Lock()

#the joystick calls the method to move a block twice
#I think this is because the joystick counts pushing it
#down and up as two, but im not sure

#to fix this I use a boolean to toggle the method so it only gets called once
toggleLeft = True
toggleRight = True
toggleDown = True

#this is our 2 d array 64 lights
ourArr = [[0 for x in range(row)] for y in range(row)]

#######################################################
    #this section is for moving pixles (WORKS CUS ME SMART)



#moves the pixle down one space
def moveDown():
    global xBlock
    global yBlock
    
    
    #waits to get a lock
    with lock:
        #checks if we would go out of bounds and does nothing if we would
        if xBlock != row-1:
            ourArr[xBlock][yBlock] = reset
            ourArr[xBlock + 1][yBlock] = white
            xBlock = xBlock +1
    setPixles()
    
#moves the block down, but this is for the joystick
def moveDownPush():
    global xBlock
    global yBlock
    global toggleDown
    
    if toggleDown:
        #waits to get a lock
        with lock:
            if xBlock != row-1:
                #checks if we would go out of bounds and does nothing if we would
                if ourArr[xBlock + 1][yBlock] != white:
                    ourArr[xBlock][yBlock] = reset
                    ourArr[xBlock + 1][yBlock] = white
                    xBlock = xBlock +1
        setPixles()
    toggleDown = not toggleDown
    
#moves the pixle left
def moveLeft():
    global xBlock
    global yBlock
    global toggleLeft
    
    if toggleLeft:
        #waits to get a lock
        with lock:
            #checks if the left block is empty
            if yBlock != 0:
                #checks if we would go out of bounds and does nothing if we would
                if ourArr[xBlock][yBlock-1] != white:
                    ourArr[xBlock][yBlock] = reset
                    ourArr[xBlock][yBlock-1] = white
                    yBlock = yBlock-1
        setPixles()
    toggleLeft = not toggleLeft    
#moves the pixle right
def moveRight():
    global xBlock
    global yBlock
    global toggleRight
    
    if toggleRight:
        #waits to get a lock
        with lock:
            #checks if the right block is empty
            if yBlock != row-1:
                #checks if we would go out of bounds and does nothing if we would
                if ourArr[xBlock][yBlock+1] != white:
                    ourArr[xBlock][yBlock] = reset
                    ourArr[xBlock][yBlock+1] = white
                    yBlock = yBlock+1
        setPixles()
    toggleRight = not toggleRight
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
def setPixles():
    #covert our 2D to a list
    global ourArr
    pixleList = convertToList(ourArr)
    #set the list to pixles
    sense.set_pixels(pixleList)
    
##############################################
    
#function to do some things on startup
def start():
    #Clear out the sense hat
    sense.clear()

    #define what happens when the user presses left or right
    sense.stick.direction_left = moveLeft
    sense.stick.direction_right = moveRight
    sense.stick.direction_down = moveDownPush

    #Has tetris scroll across the screen
    sense.show_message("Tetris", 0.1 , blue)
    sense.clear()

#spawns a new block at the top of our arr
def spawnBlock():
    #assign a starting pixle
    global xBlock
    global yBlock
    global ourArr
    
    ourArr[0][3] = white
    xBlock = 0
    yBlock = 3
    setPixles()
    time.sleep(1)
    
#prints out our list of pixles
def printList(pixleList):
    for i in pixleList:
        print(i)

#checks if the block is at the bottom row or if its above another block
def checkStop():
    global xBlock
    global yBlock
    #check if we are on the bottom row
    if xBlock >= row-1:
        return True
    #check if the space below is full
    if ourArr[xBlock+1][yBlock] == white:
        return True
    return False

#################################################
#row methods - this is for anything to do with moving, clearing or anything else to do with rows

#clears any full rows
def clearRows():
    #loop thru the rows
    for x in range(row):
        fullRow = True
        #if the first square is not white skip checking the rest for that row
        if ourArr[x][0] == white:
            for y in range(row):
                #if we find a square thats not white set full row to false
                if ourArr[x][y] != white:
                    fullRow = False
            #if row is full clear it
            if fullRow:
                removeRow(x)

#sets the row to reset
def removeRow(rowToRemove):
    for y in range(row):
        ourArr[rowToRemove][y] = reset
    blockGravity(rowToRemove)

#makes all the blocks fall down
def blockGravity(rowToStart):
    #if we are at the top of our arr, just automaticly move that row down one
    if rowToStart == 0:
        moveRowDown(0)
        return
    #we want to loop thru the row above rowToStart
    for y in range(row):
        #if we find a white block we know we need to move the whole row down
        if ourArr[rowToStart-1][y] == white:
            #move our row down
            moveRowDown(rowToStart-1)
            blockGravity(rowToStart - 1)
            break
        
#moves the row above into the row below
def moveRowDown(RowToMove):
    if RowToMove == (row -1):
        return
    for y in range(row):
        if ourArr[RowToMove][y] == white:
            ourArr[RowToMove -1][y] = white
            ourArr[RowToMove][y] = reset
        
##############################################################
    # the 'main'

start()

#Now get a list of pixles (Should be all blank)
ourArr = convertTo2D(sense.get_pixels())

spawnBlock()
setPixles()

time.sleep(speed)

is_bottom = False
        
#keep repeting untill we reach the bottom
while is_bottom == False:
    print("main " + str(xBlock) + str(yBlock))
    if checkStop():
        #spawn in a new block
        spawnBlock()
    else:
        #move our block down one
        moveDown()
        #check if there is a full row and clears it
        clearRows()
        
        setPixles()
        #this gives us a pause after each move
        time.sleep(speed)

print("Done")

