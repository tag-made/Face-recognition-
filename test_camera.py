# test_camera.py
import cv2
import time

print("--- Starting Camera Test ---")

# --- Attempt to open the camera ---
# We will try the most reliable backend first.
print("Attempting to open camera with DSHOW backend...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(2) # Give the camera time to initialize

# If that fails, try the default backend
if not cap.isOpened():
    print("DSHOW backend failed. Trying default backend...")
    cap = cv2.VideoCapture(0)
    time.sleep(2)

# --- Check if the camera was successfully opened ---
if not cap.isOpened():
    print("\n[FATAL ERROR]: Could not open the camera.")
    print("Please check the following:")
    print("1. Is the camera connected properly?")
    print("2. Is the lens cap off?")
    print("3. Is another application (Zoom, Teams, etc.) using the camera?")
    print("4. Have you tried a different USB port?")

else:
    print("\nCamera opened successfully! A window should appear.")
    print("Press 'q' on your keyboard while the window is active to quit.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # 'ret' will be False if no frame is captured
        if not ret:
            print("Error: Can't receive frame (the video stream might have ended). Exiting.")
            break
        
        # Display the resulting frame in a window
        cv2.imshow('Camera Test | Press Q to Quit', frame)
        
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(1) == ord('q'):
            break
            
    # When everything is done, release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
    print("Camera resources released successfully.")