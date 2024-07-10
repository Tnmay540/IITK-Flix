import socket, cv2, pickle, struct
serverPort = 12000
serverIP = "127.0.0.1"
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverIP, serverPort))  # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = clientSocket.recv(4 * 1024)  # 4K          #since the server sends length of serialized frame data followed by actual serialized frame
        if not packet: break                                #we first need to extract length of frame then actual frame
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:                 #this portion of code recieves and displays actual frame data
        data += clientSocket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    if cv2.imshow("RECEIVING VIDEO", frame):
        print(2)
    key = cv2.waitKey(1) & 0xFF                       # press q to exit streaming
    if key == ord('q'):
        break
clientSocket.close()