import cv2
import numpy as np
import socket
import pickle
import struct

# Set up client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8888))

# Loop for receiving and displaying video frames
while True:
    # Receive frame header
    frame_header = client_socket.recv(4)
    frame_size = struct.unpack('!I', frame_header)[0]
    
    # Receive frame data
    frame_data = b''
    while len(frame_data) < frame_size:
        frame_data += client_socket.recv(4096)
    
    # Deserialize frame data and water level information
    frame, water_level = pickle.loads(frame_data)
    
    # Convert received bytes to video frame
    frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    # Display video frame and water level information
    cv2.imshow('Video Stream', frame)
    print('Water Level:', water_level)
    
    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close client socket
client_socket.close()
cv2.destroyAllWindows()
