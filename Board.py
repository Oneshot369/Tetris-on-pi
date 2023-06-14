class Board:
    
    ##Define some stuff first
    #these are private
    row = 8
    ourArr = [[0 for x in range(row)] for y in range(row)]
    
    #initalization methos(when you create the object)
     def __init__():
         xBlock = 0
         yBlock = 0

######################################        
    #Conversion methods
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
    toggleLeft = True
    toggleRight = True
    toggleDown = True

    #######################################################
        #this section is for moving pixles 
    #--------------------------------------
        #these are for moving a whole block
    #moves down a whole block
    def moveDownBlock():
        global xBlock
        global yBlock
        global currentBlockType
        isValid = True
        
        #waits to get a lock
        with lock:
            for x in currentBlockType:
                #checks if we would go out of bounds and sets isValid to false if we would
                if (xBlock + x[0]) >= row-1:
                    isValid = False
            #if we wont go out of bounds we move our block
            if isValid:
                for x in currentBlockType:
                    ourArr[xBlock + x[0]][yBlock + x[1]] = reset
                for x in currentBlockType:
                    ourArr[xBlock + 1 + x[0]][yBlock + x[1]] = white
                xBlock = xBlock +1
        setPixles()

    #moves a whole block left
    def moveLeftBlock():
        global xBlock
        global yBlock
        global toggleLeft
        global currentBlockType
        isValid = True
        
        if leftClear():
            if toggleLeft:
                #waits to get a lock
                with lock:
                    for x in currentBlockType:
                        #checks if we would go out of bounds and sets isValid to false if we would
                        if (yBlock + x[1]) <= 0:
                            isValid = False
                    #moves all pixles left one
                    if isValid:
                        for x in currentBlockType:
                            ourArr[xBlock + x[0]][yBlock + x[1]] = reset
                        for x in currentBlockType:
                            ourArr[xBlock + x[0]][yBlock + x[1] - 1] = white
                        yBlock = yBlock -1
                setPixles()
            toggleLeft = not toggleLeft

    #moves a whole block right   
    def moveRightBlock():
        global xBlock
        global yBlock
        global toggleRight
        global currentBlockType
        isValid = True
        
        if rightClear():
            if toggleRight:
                #waits to get a lock
                with lock:
                    #loops thru our block
                    for x in currentBlockType:
                        #checks if we would go out of bounds and sets isValid to false if we would
                        if (yBlock + x[1]) >= row-1:
                            isValid = False
                    #moves all pixles left one
                    if isValid:
                        for x in currentBlockType:
                            ourArr[xBlock + x[0]][yBlock + x[1]] = reset
                        for x in currentBlockType:
                            ourArr[xBlock + x[0]][yBlock + x[1] + 1] = white
                        yBlock = yBlock + 1
                setPixles()
            toggleRight = not toggleRight

    #moves a whole block down by one
    def moveDownPushBlock():
        global xBlock
        global yBlock
        global toggleDown
        isValid = True
        if not checkStopBlock():
            if toggleDown:
                #waits to get a lock
                with lock:
                    for x in currentBlockType:
                        #checks if we would go out of bounds and sets isValid to false if we would
                        if (xBlock + x[0]) >= row-1:
                            isValid = False
                    #if we wont go out of bounds we move our block
                    if isValid:
                        for x in currentBlockType:
                            ourArr[xBlock + x[0]][yBlock + x[1]] = reset
                        for x in currentBlockType:
                            ourArr[xBlock + 1 + x[0]][yBlock + x[1]] = white
                        xBlock = xBlock +1
                setPixles()
        toggleDown = not toggleDown
    #Checks right if it is clear
    def rightClear():
        global xBlock
        global yBlock
        global currentBlockType
        #check if we are on the bottom row
        if xBlock >= row-1:
            return True
        #check if the space below ourBlock is full
        for x in currentBlockType:
            #checks is the space below is white
            if (ourArr[xBlock + x[0]][yBlock + x[1]+1]) == white:
                return True
        return False

    #checks if the left is clear
    def leftClear():
        global xBlock
        global yBlock
        global currentBlockType
        #check if we are on the left colunm 
        if xBlock >= 0:
            return True
        #check if the space below ourBlock is full
        for x in currentBlockType:
            #checks is the space below is white
            if (ourArr[xBlock + x[0]][yBlock + x[1]-1]) == white:
                return True
        return False

    #checks if the block is at the bottom row or if its above another block
    def checkStopBlock():
        global xBlock
        global yBlock
        global currentBlockType
        #check if we are on the bottom row
        if xBlock >= row-1:
            return True
        #check if the space below ourBlock is full
        for x in currentBlockType:
            #checks is the space below is white
            if (ourArr[xBlock + x[0] + 1][yBlock + x[1]]) == white:
                return True
        return False

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
        setPixles()
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
        setPixles()
            
    #moves the row above into the row below
    def moveRowDown(RowToMove):
        if RowToMove == (row -1):
            return
        for y in range(row):
            if ourArr[RowToMove][y] == white:
                ourArr[RowToMove + 1][y] = white
                ourArr[RowToMove][y] = reset
       
    ##############################################################
