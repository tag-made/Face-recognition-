# create_dataset.py
import cv2
import face_recognition
import pickle
import os

# Path to the folder of student images
images_folder_path = 'ImagesAttendance'
path_list = os.listdir(images_folder_path)

print("Loading images...")
image_list = []
student_data = [] # Will store the names/IDs

for path in path_list:
    # Read the image file
    img = cv2.imread(os.path.join(images_folder_path, path))
    
    if img is not None:
        image_list.append(img)
        # Extract the name/ID from the filename
        student_data.append(os.path.splitext(path)[0])
    else:
        print(f"Warning: Could not read image {path}")

def find_encodings(images):
    """Processes a list of images and returns their face encodings."""
    encode_list = []
    print("Calculating encodings... this may take a while for many images.")
    
    for i, img in enumerate(images):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img_rgb)
        if encodes:
            encode_list.append(encodes[0])
        else:
            print(f"Warning: No face found in {student_data[i]}.jpg. Skipping.")
            
    return encode_list

known_encodings = find_encodings(image_list)
encodings_with_ids = [known_encodings, student_data]
print("Encoding complete.")

# The 'encodings.pkl' file is your dataset.
with open('encodings.pkl', 'wb') as f:
    pickle.dump(encodings_with_ids, f)

print("Dataset created and saved successfully as 'encodings.pkl'")