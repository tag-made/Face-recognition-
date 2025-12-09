Face Recognition – Local Web App
This is a local face recognition web app that identifies Elon Musk, Bill Gates, and Andrew Tate from a live webcam feed and logs each successful recognition with the current date and time into a CSV file. The backend is written in Python, and the user interface is built with HTML/CSS served from a lightweight web server.

Features
Real-time face recognition from your webcam for three known identities: Elon Musk, Bill Gates, and Andrew Tate.

Simple browser-based UI to start the camera stream and view recognition feedback.

Automatic attendance logging into a CSV file (name, date, time) whenever a known face is detected.

Cooldown logic so the same person is not spam-logged repeatedly within a short window.

Designed to run fully on your local machine for privacy and easier experimentation.

Tech Stack
Python for the backend face recognition logic and attendance handling.

OpenCV for webcam access and basic image processing.

face_recognition (built on top of dlib) for face detection, encodings, and comparison.​

Flask (or similar Python web framework) to serve the HTML pages and webcam video stream.

HTML + CSS for the user interface (main page and attendance page).

CSV file (Attendance.csv) for logging recognized faces with timestamps.

Project Overview
A precomputed encodings file (e.g., encodings.pkl) stores face embeddings and labels for the three supported identities.

A main Python app script starts a web server, opens the camera, runs face recognition in a loop, draws bounding boxes and labels on detected faces, and streams the processed frames to the browser.

Each time a known face is recognized, the app appends a new row to the CSV log with the person’s name and the current date/time, then shows visual feedback in the video feed.

Separate HTML pages are used for the live camera view and for displaying the attendance table rendered from the CSV file.

Getting Started
Clone the repository

bash
git clone https://github.com/tag-made/Face-recognition-.git
cd Face-recognition-
Create and activate a virtual environment (optional but recommended)

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies (for example):

bash
pip install opencv-python face_recognition flask pandas numpy
Ensure encodings exist

Make sure your face encodings file (e.g., encodings.pkl) is present in the project root.

If you have a dataset script (like create_dataset.py), run it first to generate/update encodings for Elon Musk, Bill Gates, and Andrew Tate.

Run the app

bash
python app.py
Then open the printed URL in your browser (typically http://127.0.0.1:5000/) to access the UI.

Usage
Open the main page in your browser and allow camera access.

Position your face (or a printed photo) in front of the webcam; if it matches Elon Musk, Bill Gates, or Andrew Tate, the app will draw a rectangle, show the detected name, and log the event into the CSV file with the current timestamp.

Visit the attendance page from the UI to see a table view of all logged recognitions loaded from the CSV file.

Stop the server or close the browser tab when you’re done.

Limitations & Future Improvements
Currently restricted to three known identities; you can extend it by adding more images, regenerating encodings, and updating labels.

Designed for local use only; not yet deployed to a public server or cloud.

Possible improvements: better UI/UX, admin controls to clear or export logs, support for multiple cameras, and a configuration page to add new people dynamically.
