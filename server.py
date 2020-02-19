import sys
import socket

###this was so confusing and took me so long and we are very sorry about the terrible code
###we'll make sure its better next time :/

hostName = socket.gethostname()
ipAddress = socket.gethostbyname(hostName)
print("ur ip is " + ipAddress)
global columns
columns = 10
global rows
rows = 10
response = ""
global hitMark
hitMark = "X"
global emptyMark
emptyMark = "_"

global shipC
shipC = 5
global shipB
shipB = 4
global shipR
shipR = 3
global shipS
shipS = 3
global shipD
shipD = 2


port = int(sys.argv[1])
inputFile = open(sys.argv[2])
global localBoard
localBoard = [[emptyMark for i in range(columns)] for j in range(rows)] #found how to initialize 2d array at https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
global opBoard
opBoard =    [[emptyMark for i in range(columns)] for j in range(rows)]

def printBoard(board):
    for i in range(columns):
        print("\n")
        for j in range(rows):
            print(board[i][j] + " ", end = "")

def text2Array(board, textFile):
    for i in range(columns):
        for j in range(rows + 1):
            if j == rows:
                textFile.read(1) #this gets rid of line return 
            else:
                board[i][j] = textFile.read(1) #puts one char into the array from the text file

def checkFire(x, y):
    global shipC
    global shipB
    global shipR
    global shipS
    global shipD
    global hitMark
    global emptyMark
    global columns
    global rows
    global localBoard
    #print(x,y)
    temp = 0
    y = rows - y #this is necissary because the way a 2d array reads y input is opposite of how an actual graph is plotted
    temp = y
    y = x
    x = temp-1

    #print(x,y)
    if localBoard[x][y] == hitMark:
        response = "410" #if spot has already been hit, HTTP gone message sent

    elif localBoard[x][y] == emptyMark:
        localBoard[x][y] = hitMark
        response = "hit=0"
        

    elif localBoard[x][y] == "C":
        localBoard[x][y] = hitMark
        shipC -= 1
        if shipC == 0:
            response = "hit=1&sunk=C"
        else:
            response = "hit=1"

    elif localBoard[x][y] == "B":
        localBoard[x][y] = hitMark
        shipB -= 1
        if shipB == 0:
            response = "hit=1&sunk=B"
        else:
            response = "hit=1"
        
    elif localBoard[x][y] == "R":
        localBoard[x][y] = hitMark
        shipR -= 1
        if shipR == 0:
            response = "hit=1&sunk=R"
        else:
            response = "hit=1"
        
        
    elif localBoard[x][y] == "S":
        localBoard[x][y] = hitMark
        shipS -= 1
        if shipS == 0:
            response = "hit=1&sunk=S"
        else:
            response = "hit=1"
            
    elif localBoard[x][y] == "D":
        localBoard[x][y] = hitMark
        shipD -= 1
        if shipD == 0:
            response = "hit=1&sunk=D"
        else:
            response = "hit=1"

    else:
        response = "404"
        

    return response


def findWord(word, text):
    result = text.find(word)
    return result

    
##    for i in range(len(text)):
##        if text[i] == word[0]
##        
##        for j in range(len(word)):
##            if text[i+j] == word[j]:
##                if len(word) == j:
##                    return "found"
##                
##            else:
##                break
                




def decodeMessage(message):
    if "GET /own_board.html" in message:
        printBoard(localBoard)
        response = localBoard

    if "GET /opponent_board.html" in message:
        printBoard(opBoard)
        response = opBoard

    elif message[findWord("x=", message) + 2] == "-" or message[findWord("y=", message) + 2] == "-":
        response = "404" #404 not found this coordinate is outa bounds

    elif message[findWord("x=", message) + 3] != "&":
        response = "404" #if either coordinate is more than 1 digit then its more than 9 so, out of bounds

    

    elif message[0] != "h":
        xCoord = int(message[findWord("x=", message) + 2])
        yCoord = int(message[findWord("y=", message) + 2])
        #print(xCoord, ",", yCoord)
        response = checkFire(xCoord, yCoord)

    elif message[0] == "h":
        temp = 0
        y = rows - y #this is necissary because the way a 2d array reads y input is opposite of how an actual graph is plotted
        temp = y
        y = x
        x = temp
        oppBoard[x][y] = "X"

    #print(response)
    return response





text2Array(localBoard, inputFile)
#print(response)
#printBoard(localBoard)
host = socket.gethostbyname(socket.gethostname())
sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSocket.bind(("",port))
sSocket.listen(1)
print("Server ready")
#printBoard(opBoard)
print("\n_______________________________")
printBoard(localBoard)

while 1:    # listen for input
    cSocket, addr = sSocket.accept()
    message = cSocket.recv(1024)
    response = decodeMessage(message.decode('iso-8859-1'))

    conType = 'close'
    contType = 'x-www-form-urlencoded'
    contLength = str(len(response))

    if response == '404' or response == '410' or response == '400':
        reply = "HTTP/1.1 %s\r\nConnection: %s\r\nContent-Type: %s\r\nContent-Length: %s\r\n" % (response, conType, contType, contLength)

    else:
        reply = "HTTP/1.1\r\nConnection: %s\r\nContent-Type: %s\r\nContent-Length: %s\r\n%s" %(contType, contType, contLength, response)
        #printBoard(opBoard)
        printBoard(localBoard)

    cSocket.sendall(reply.encode('iso-8859-1'))
    cSocket.close()
    






