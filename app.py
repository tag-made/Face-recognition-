# app.py (Final, Most Stable Version)

from flask import Flask, render_template, Response
import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import pandas as pd
import time
import threading
import queue
import os
import sys
import traceback

# Initialize the Flask application
app = Flask(__name__)

# --- Load the Dataset ---
print("Loading dataset...")
try:
    if not os.path.exists('encodings.pkl'):
        raise FileNotFoundError("encodings.pkl not found in working directory: " + os.getcwd())

    with open('encodings.pkl', 'rb') as f:
        encode_list_known_with_ids = pickle.load(f)

    # Expecting a tuple/list of (encode_list_known, classNames)
    try:
        encode_list_known, classNames = encode_list_known_with_ids
    except Exception:
        raise ValueError("encodings.pkl does not contain the expected (encode_list_known, classNames) structure")

    # Normalize types
    if encode_list_known is None:
        encode_list_known = []
    if classNames is None:
        classNames = []

    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Failed to load encodings.pkl: {e}")
    print(traceback.format_exc())
    # It's safer to exit early than to let the server run in a broken state
    sys.exit(1)

# --- Cooldown Logic Variables ---
recent_entries = {}
COOLDOWN_PERIOD = 60 

# --- A thread-safe queue to hold processed frames ---
frame_queue = queue.Queue()

def markAttendance(name):
    """Appends the recognized name and current time to the Attendance.csv file."""
    with open('Attendance.csv', 'a+') as f:
        now = datetime.now()
        dtString = now.strftime('%Y-%m-%d %H:%M:%S')
        f.writelines(f'\n{name},{dtString}')

def video_processing_thread():
    """
    This function runs in a background thread. It continuously reads from the
    camera, performs face recognition, and puts the processed frame into a queue.
    """
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(2) # Camera warm-up

    if not camera.isOpened():
        print("Error: Background thread could not open camera.")
        return

    while True:
        success, frame = camera.read()
        if not success or frame is None:
            print("Background thread failed to grab frame.")
            time.sleep(1) # Wait a second before trying again
            continue

        try:
            # --- Face Recognition and Drawing Logic ---
            imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encode_list_known, encodeFace)
                faceDis = face_recognition.face_distance(encode_list_known, encodeFace)

                # Defensive: if there are no known encodings, skip matching
                if len(faceDis) == 0:
                    continue

                matchIndex = np.argmin(faceDis)

                # Defensive: ensure matches list is not empty and index is valid
                if not matches or matchIndex >= len(matches):
                    continue

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    
                    current_time = time.time()
                    if name not in recent_entries or current_time - recent_entries[name] > COOLDOWN_PERIOD:
                        markAttendance(name)
                        recent_entries[name] = current_time
                        feedback_text = f"MARKED: {name}"
                        cv2.putText(frame, feedback_text, (15, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    else:
                        feedback_text = "ALREADY MARKED"
                        cv2.putText(frame, feedback_text, (15, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
            
            # Put the processed frame into the queue
            frame_queue.put(frame)

        except Exception as e:
            print(f"An error occurred in video processing thread: {e}")
            print(traceback.format_exc())

def generate_frames_for_stream():
    """
    This function is a generator that pulls frames from the queue and yields
    them to the web browser.
    """
    while True:
        frame = frame_queue.get() # Get a frame from the queue
        if frame is None:
            continue
        
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames_for_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance')
def attendance():
    try:
        # To avoid errors with an empty file, check if it has content
        df = pd.read_csv('Attendance.csv')
        if df.empty:
             return "Attendance log is empty.", 200
        return render_template('attendance.html', table=df.to_html(classes='table table-striped', index=False))
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return "Attendance file not found or is empty.", 404

# --- Start the background thread ---
threading.Thread(target=video_processing_thread, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=False)