from socket import *
import pickle as p
import struct as str
import cv2
serverPort = 12000
serverIP = "127.0.0.1"
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP,serverPort))
serverSocket.listen(1)
print("The server is ready to transmit")
while True:
    connectionSocket, clientAddress = serverSocket.accept()
    print(f"Got connection from {clientAddress}")
    if connectionSocket:
        vid = cv2.VideoCapture(0)
        while vid.isOpened():
            img, frame = vid.read()
            a = p.dumps(frame)
            message = str.pack("Q", len(a)) + a                     # sends length of frame data + actual serialized frame data
            connectionSocket.sendall(message)
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                connectionSocket.close()

