import cv2
import socket
import pickle
import struct

# Set up server socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8888))
server_socket.listen(5)

print("Server is up and running...")

# OpenCV setup for video capture
cap = cv2.VideoCapture(0)  # Use camera index 0 for default camera

# Loop for capturing and sending video frames
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform water level detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Calculate frame size
        frame_height, frame_width, _ = frame.shape
        frame_size = frame_height * frame_width
        
        
        water_level = "low level"  # Default to Low
        
        for contour in contours:
            area = cv2.contourArea(contour)   
            if area > 0.5 * frame_size:  # If contour area is more than 50% of frame size, consider water level as high
                water_level = "high level"
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                cv2.putText(frame, "Water Detected: High", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                break
            else:
                cv2.drawContours(frame, [contour], -1, (0, 0, 255), 3)
                cv2.putText(frame, "Water Detected: Low", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Serialize and send video frame and water level information to client
        frame_data = pickle.dumps((frame, water_level))
        frame_size = struct.pack('!I', len(frame_data))
        client_socket.sendall(frame_size + frame_data)

    # Close client socket when video capture is stopped
    client_socket.close()

# Release video capture and close server socket
cap.release()
server_socket.close()
