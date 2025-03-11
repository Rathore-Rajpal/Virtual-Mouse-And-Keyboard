import cv2
import numpy as np
from PIL import Image
import os

# Path for the training images
path = 'assist\\Engine\\auth\\samples'

# Local Binary Patterns Histograms recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create(radius=2, neighbors=8, grid_x=8, grid_y=8)

# Haar Cascade classifier for face detection
detector = cv2.CascadeClassifier("assist\\Engine\\auth\\haarcascade_frontalface_default.xml")

def Images_And_Labels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        gray_img = Image.open(imagePath).convert('L')
        img_arr = np.array(gray_img, 'uint8')

        # Apply histogram equalization
        img_arr = cv2.equalizeHist(img_arr)

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30))

        for (x, y, w, h) in faces:
            faceSamples.append(img_arr[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait...")

faces, ids = Images_And_Labels(path)
recognizer.train(faces, np.array(ids))

# Save the trained model to a file
recognizer.write('assist\\Engine\\auth\\trainer\\trainer.yml')

print("Model trained. Now we can recognize your face.")
