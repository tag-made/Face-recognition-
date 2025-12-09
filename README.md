# 🚀 Face Recognition – Local Web App

A local, privacy-friendly face recognition web app that identifies **Elon Musk**, **Bill Gates**, and **Andrew Tate** from your webcam feed and logs each successful detection (name, date, time) into a CSV file.  

> 🎯 Built with Python for the backend and HTML/CSS for a clean, simple UI.

---

## ✨ Features

- 🧠 **Face recognition for 3 identities**  
  Detects and labels Elon Musk, Bill Gates, and Andrew Tate in real time from your webcam.

- 🖥️ **Browser-based interface**  
  Start/stop the camera and view results directly in your browser.

- 🗓️ **CSV attendance logging**  
  Automatically logs **Name · Date · Time** to a `.csv` file whenever a known face is recognized.

- 🔁 **Spam‑free logging**  
  Cooldown logic to avoid writing duplicate entries every frame for the same person.

- 🔐 **Local-only processing**  
  Everything runs on your own machine for better control and privacy.

---

## 🧰 Tech Stack

- 🐍 **Python** – core logic and web server  
- 📸 **OpenCV** – camera access and frame processing  
- 🙂 **face_recognition** – face detection, encodings, and comparison [web:101][web:112]  
- 🌐 **HTML + CSS** – user interface pages  
- 📄 **CSV** – lightweight logging of recognized faces and timestamps  

---

## 📁 Project Overview

- Precomputed encodings (e.g. `encodings.pkl`) store embeddings for  
  **Elon Musk · Bill Gates · Andrew Tate**.  
- `app.py` (or similar) starts a small web server, opens the webcam, and runs the recognition loop.  
- Each successful match:
  - Draws a rectangle and label on the video frame  
  - Appends a new row to `Attendance.csv` with `Name, Date, Time`  
- Separate HTML pages handle:
  - 🎥 Live camera view  
  - 📊 Attendance table rendered from the CSV file  

---

## 🚀 Getting Started

1. **Clone the repository**
git clone https://github.com/tag-made/Face-recognition-.git
cd Face-recognition-

text

2. **(Optional) Create a virtual environment**
python -m venv venv

Windows
venv\Scripts\activate

Linux / macOS
source venv/bin/activate

text

3. **Install dependencies**
pip install opencv-python face_recognition flask pandas numpy

text

4. **Ensure face encodings exist**
- Keep your encodings file (e.g. `encodings.pkl`) in the project root.  
- If you have a dataset/encoder script, run it first to (re)generate encodings for the three people.

5. **Run the app**
python app.py

text
Then open the URL shown in the terminal (usually `http://127.0.0.1:5000/`) in your browser and allow camera access.

---

## 🎮 How to Use

- Open the main page → click the button to start the camera stream.  
- Show a face (or photo) of Elon Musk, Bill Gates, or Andrew Tate to the webcam.  
- When a match is found:
- The name appears on the video frame.
- A new record is written to `Attendance.csv` with the current date and time.  
- Visit the attendance/records page in the UI to see a table of all logs.  
- Stop the server (Ctrl+C in terminal) when finished.

---

## 🔮 Future Improvements

- ➕ Add support for more people via a simple “upload & encode” flow.  
- 🌍 Deploy to a remote server with authentication for multi-user access.  
- 🧾 Export logs as Excel/JSON and add filters/search in the attendance UI.  
- 🎨 Enhance UI with better styling, dark mode, and mobile responsiveness.

---

## 💡 Note

This project is meant for **learning and experimentation** with face recognition and basic web integration.  
Please always respect privacy, consent, and local laws when using face recognition technology.
You can also add badges (e.g. Python version, license, status) right under the main title to make the README even more scannable and professional.​
