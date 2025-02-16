import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
]

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (200, 0, 200), cv2.FILLED)
        cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 2)
    return img

class Button:
    def __init__(self, pos, text, size=[80, 70]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()  # Capture frame from webcam

    # Detect hands in the image
    hands, img = detector.findHands(img)  # Detect hands and landmarks

    # Initialize lmList to avoid NameError
    lmList = []

    # Check if any hands are detected
    if hands:
        # Get the first hand detected
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 hand landmarks
        bbox = hand["bbox"]

    # Draw buttons
    img = drawAll(img, buttonList)

    # Check if a finger is over a button
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 255), 2)

                # Get the distance between index finger (id 8) and middle finger (id 12)
                try:
                    result = detector.findDistance(8, 12, img)

                    # Ensure that findDistance returned a tuple with 3 elements
                    if isinstance(result, tuple) and len(result) == 3:
                        l, _, _ = result  # Unpack only if it's a valid tuple

                        # Print the distance
                        print(f"Distance between index and middle finger: {l}")
                except Exception as e:
                    pass  # Handle exception gracefully

    # Display the image
    cv2.imshow("Image", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
