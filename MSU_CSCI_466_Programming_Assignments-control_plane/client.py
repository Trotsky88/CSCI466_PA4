import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])
x = int(sys.argv[3])
y = int(sys.argv[4])
stringCoord = "x="
stringCoord = stringCoord + str(x) + "&y=" + str(y)


def findWord(word, text):
    result = text.find(word)
    return(word)

def decodeMessage(message):
    if "sunk" in message:
        print("Sunk a ship")

    elif "hit=1" in message:
        print("HIT!")
        
    elif "hit=0" in message:
        print("Missed!")


    #print(message)


cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cSocket.connect((host, port))
conType = "close"
content = stringCoord
contType = "application/x-www-form-urlencoded"
contLength = str(len(content))
user = "client.py"
#print(stringCoord)

post = "POST / HTTP/1.1\r\nConnection: %s\r\nContent-type: %s\r\nUser-Agent: %s\r\nContent-Length: %s\r\n%s" % (conType, contType, user, contLength, content)

cSocket.send(post.encode("iso-8859-1"))
response = cSocket.recv(1024).decode()
#print("response = ", response, "\n")

if "404" in response:
    print("404 not found")

elif "410" in response:
    print("410 gone")

elif "400" in response:
    print("400 bad request")

else:
    decodeMessage(response)

cSocket.close()
