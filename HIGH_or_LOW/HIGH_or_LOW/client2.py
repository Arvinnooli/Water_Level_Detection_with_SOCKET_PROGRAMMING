import cv2
import numpy as np
import socket
import pickle
import struct

# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8888))

# OpenCV setup for video display
cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video Stream", 640, 480)

# Loop for receiving and displaying video frames
while True:
    # Receive frame size
    frame_size_data = b''
    while len(frame_size_data) < 4:
        frame_size_data += client_socket.recv(4 - len(frame_size_data))
    frame_size = struct.unpack('!I', frame_size_data)[0]
    
    # Receive frame data
    frame_data = b''
    while len(frame_data) < frame_size:
        frame_data += client_socket.recv(frame_size - len(frame_data))
    
    # Deserialize frame data and extract frame and water level information
    frame, water_level = pickle.loads(frame_data)
    
    # Display received frame
    cv2.imshow("Video Stream", frame)
    print("Water Level:", water_level)
    
    # Exit loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close client socket and destroy OpenCV window
client_socket.close()
cv2.destroyAllWindows()
