import cv2
import pyautogui as p

def AuthenticateFace():
    flag = ""
    
    # Load the trained LBPH face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('assist\\Engine\\auth\\trainer\\trainer.yml')

    # Load the Haar Cascade for face detection
    faceCascade = cv2.CascadeClassifier("assist\\Engine\\auth\\haarcascade_frontalface_default.xml")

    font = cv2.FONT_HERSHEY_SIMPLEX  # Font for text on the image

    # Name mappings (index 1 corresponds to "Raj")
    names = ['', 'Raj']

    # Initialize webcam
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # Set width of the frame
    cam.set(4, 480)  # Set height of the frame

    # Minimum window size for a face to be recognized
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply histogram equalization
        converted_image = cv2.equalizeHist(converted_image)

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Predict the face's ID and accuracy
            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])

            # If accuracy is below 75%, consider it a match
            if accuracy < 75:
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 1
            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
                flag = 0

            # Display the name and accuracy on the video feed
            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        # Show the video feed with the rectangles and text
        cv2.imshow('camera', img)

        # Exit if 'ESC' is pressed
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
        if flag == 1:
            break

    # Release the camera and close all OpenCV windows
    cam.release()
    cv2.destroyAllWindows()

    return flag



