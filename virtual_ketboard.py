import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)

# Define the keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
]
finalText = ""

# Function to draw all buttons on the image
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw button background with a slight shadow
        cv2.rectangle(img, (x + 5, y + 5), (x + w + 5, y + h + 5), (50, 50, 50), cv2.FILLED)  # Shadow
        cv2.rectangle(img, button.pos, (x + w, y + h), (200, 0, 200), cv2.FILLED)  # Button itself
        # Center the text
        text_size = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_COMPLEX, 1.2, 2)[0]  # Adjust text size
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, button.text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
    return img

# Button class to define each key's properties
class Button:
    def __init__(self, pos, text, size=[75, 65]):  # Reduced size for smaller buttons
        self.pos = pos
        self.size = size
        self.text = text

# Create a list of Button objects for the keyboard
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([90 * j + 50, 90 * i + 150], key))  # Reduced spacing between buttons

# Main loop
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
        lmList = hand["lmList"]  # List of 21 hand landmarks (x, y, z)
        bbox = hand["bbox"]

    # Draw buttons on the image
    img = drawAll(img, buttonList)

    # Check if a finger is over a button
    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # Check if the index finger tip (landmark 8) is over the button
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                # Highlight the button
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)

                # Get only x,y coordinates (ignore z-axis)
                p8 = lmList[8][0:2]  # Index finger tip (x, y)
                p4 = lmList[4][0:2]  # Thumb finger tip (x, y)

                # Calculate distance between thumb and index finger tips
                length, _, _ = detector.findDistance(p8, p4, img)
                print(f"Distance between thumb and index finger: {length}")

                # Detect click when thumb and index finger tips are close enough
                if length < 35:  # Adjust this threshold as needed
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
                    finalText += button.text

    # Draw the text box below
    cv2.rectangle(img, (50, 500), (1180, 600), (0, 255, 0), cv2.FILLED)  # Make the box wider to fit more text
    cv2.putText(img, finalText, (60, 570), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 3)  # Adjust font size and position

    # Display the image
    cv2.imshow("Virtual Keyboard", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
