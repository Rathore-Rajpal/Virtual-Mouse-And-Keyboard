import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller, Key

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1580)  # Set width
cap.set(4, 720)   # Set height

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)

# Define the expanded keyboard layout
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "BS"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "Shift"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Enter"],
    ["Space"]
]

finalText = ""
keyboard = Controller()

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
    def __init__(self, pos, text, size=[85, 65]):  # Slightly smaller buttons
        self.pos = pos
        self.size = size
        self.text = text

# Create a list of Button objects for the keyboard
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        # Adjust button width for Space, Enter, and Backspace
        if key == "Space":
            buttonList.append(Button([90 * j + 50, 90 * i + 150], key, size=[500, 65]))  # Wider space bar
        elif key == "Enter" or key == "BS" or key == "Shift":
            buttonList.append(Button([90 * j + 50, 90 * i + 150], key, size=[170, 65]))  # Wider Enter and Backspace
        else:
            buttonList.append(Button([90 * j + 50, 90 * i + 150], key))  # Default button size

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
                    # Handle special keys like Space, Enter, Shift, and Backspace separately
                    if button.text == "Space":
                        finalText += " "
                        keyboard.press(Key.space)
                        keyboard.release(Key.space)
                    elif button.text == "Enter":
                        finalText += "\n"
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                    elif button.text == "BS":
                        finalText = finalText[:-1]
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                    elif button.text == "Shift":
                        # Optional: Implement Shift key functionality, if needed
                        pass
                    else:
                        keyboard.press(button.text)
                        keyboard.release(button.text)
                        finalText += button.text

                    # Change button color to green after click
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 25, y + 55), cv2.FONT_HERSHEY_COMPLEX, 1.2, (255, 255, 255), 2)
                    sleep(0.25)

    # Display the image
    cv2.imshow("Virtual Keyboard", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()