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
    ["A", "S", "D", "F", "G", "H", "J", "K", "L",";"],
    ["Z", "X", "C", "V", "B", "N", "M",",",".","/"]
]

def drawAll(img, buttonList):

    for button in buttonList:
      x,y = button.pos
      w,h = button.size
      cv2.rectangle(img,button.pos,(x+w,y+h),(200,0,200),cv2.FILLED)
      cv2.putText(img, button.text , (x+15,y+50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,255), 2)


class Button():
    def __init__(self,pos, text, size = [60,70]):
        self.pos = pos
        self.size = size
        self.text = text
        
        

buttonList = []
for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
           buttonList.append(Button([100 * j + 10, 100 * i +50],key))   


while True:
    success, img = cap.read()  # Capture frame from webcam

    # Detect hands in the image
    hands, img = detector.findHands(img)  # Detect hands and landmarks

    # Check if any hands are detected
    if hands:
        # Get the first hand detected
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 hand landmarks
        bbox = hand["bbox"]   

   
    #img = myButton.draw(img)
    # Display the image
    cv2.imshow("Image", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
