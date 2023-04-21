import cv2
import numpy as np
import socket
import pickle
import struct
import keyboard  # Import keyboard module for key press detection

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8888))
server_socket.listen(5)

print('Waiting for client connection...')

# Accept client connection
client_socket, client_address = server_socket.accept()
print(f'Client connected: {client_address}')

# OpenCV setup for video capture
cap = cv2.VideoCapture(0)

# Loop for capturing and sending video frames
while True:
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform pixel intensity thresholding
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # Compute water level as percentage of white pixels
    total_pixels = thresh.size
    white_pixels = cv2.countNonZero(thresh)
    water_level = (white_pixels / total_pixels) * 100

    # Convert frame to JPEG format
    ret, frame = cv2.imencode('.jpg', frame)

    # Serialize frame data and water level information
    frame_data = pickle.dumps((frame, water_level))

    # Create frame header with size
    frame_size = len(frame_data)
    frame_header = struct.pack('!I', frame_size)

    # Send frame header and frame data
    client_socket.sendall(frame_header + frame_data)

    # Check for key press to terminate the loop
    if keyboard.is_pressed('q'):
        print('Terminating...')
        break

# Close server socket, client socket, and release video capture
server_socket.close()
client_socket.close()
cap.release()
