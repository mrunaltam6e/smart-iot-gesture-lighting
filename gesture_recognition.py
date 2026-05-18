import cv2
import mediapipe as mp
import serial
import time

# --- 1. SERIAL CONFIGURATION ---
# Replace 'COM3' with your actual port (e.g., '/dev/ttyACM0' on Linux or Mac)
SERIAL_PORT = 'COM3' 
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow Arduino connection to stabilize
    print(f"Successfully connected to Arduino on {SERIAL_PORT}")
except Exception as e:
    print(f"Warning: Could not connect to serial port {SERIAL_PORT}. Running in simulation mode.")
    print(f"Error details: {e}")
    arduino = None

# --- 2. MEDIAPIPE INITIALIZATION ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Initialize Hand tracking pipeline
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Open system default camera
cap = cv2.VideoCapture(0)

print("Starting Gesture Tracking... Press 'q' to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip horizontally for a natural selfie-view, then convert to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to get landmarks
    results = hands.process(rgb_frame)
    
    finger_count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw tracking wireframe on the screen
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract the 21 localized landmark coordinates
            landmarks = hand_landmarks.landmark
            
            # Indices for 4 fingers (Tip, Middle-Joint)
            # 8: Index, 12: Middle, 16: Ring, 20: Pinky
            finger_tips = [8, 12, 16, 20]
            
            # Check if fingers are up (Comparing Tip Y-coordinate against lower Joint Y-coordinate)
            # In computer vision screen space, a lower Y value means the point is higher up on screen
            for tip in finger_tips:
                if landmarks[tip].y < landmarks[tip - 2].y:
                    finger_count += 1
                    
            # Special logic for Thumb (Horizontal tracking comparison: Tip X vs Joint X)
            # Assumes right hand / standard camera configuration orientation
            if landmarks[4].x > landmarks[3].x:
                finger_count += 1

        # --- 3. STREAM DATA TO ARDUINO ---
        if arduino:
            # Your Arduino code uses Serial.parseInt(), so we send the number followed by a newline separator
            arduino.write(f"{finger_count}\n".encode())
            
    # Overlay the active finger count directly onto the video display window
    cv2.putText(
        frame, f'Fingers: {finger_count}', (20, 70), 
        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3
    )
    
    # Render the interactive frame window
    cv2.imshow('Smart IoT Lighting Control Hub', frame)
    
    # Break frame execution loop instantly on 'q' keyboard trigger
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up resource allocations safely
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
print("System resources released cleanly.")