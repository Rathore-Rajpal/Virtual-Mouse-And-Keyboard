import cv2
import mediapipe as mp
import util
import pyautogui
from pynput.mouse import Button, Controller
import random
import functions
from pyautogui import FailSafeException

mouse = Controller()
drawing_mode = False  # To toggle drawing mode
screen_width, screen_height = pyautogui.size()
SMOOTHING_FACTOR = 0.4

# Scaling factor to make reaching corners easier (increase this to make navigation easier)
SCALING_FACTOR_X = 1.7  # Scale movement in the x direction
SCALING_FACTOR_Y = 1.7  # Scale movement in the y direction

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

prev_x, prev_y = 0, 0  # Previous finger tip position for drawing


def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
    return None

def smooth_movement(new_x, new_y, prev_x, prev_y):
    smooth_x = int(prev_x * (1 - SMOOTHING_FACTOR) + new_x * SMOOTHING_FACTOR)
    smooth_y = int(prev_y * (1 - SMOOTHING_FACTOR) + new_y * SMOOTHING_FACTOR)
    return smooth_x, smooth_y

def move_mouse_safe(x, y):
    try:
        pyautogui.moveTo(x, y)
    except FailSafeException:
        print("Fail-safe triggered! Mouse moved to a corner of the screen.")

def move_mouse(index_finger_tip):
    global prev_x, prev_y, drawing_mode

    if index_finger_tip is not None:
        # Get raw normalized coordinates (0-1) from landmarks
        normalized_x = index_finger_tip.x
        normalized_y = index_finger_tip.y

        # Adjust scaling dynamically based on the position in the frame
        # Limit the scaling to ensure hand doesn't move too far out of view
        if normalized_x < 0.1:  # Near left edge
            scale_x = 0.8  # Reduce scaling on X-axis when near the edge
        elif normalized_x > 0.9:  # Near right edge
            scale_x = 0.8
        else:
            scale_x = SCALING_FACTOR_X  # Normal scaling in the center region

        if normalized_y < 0.1:  # Near top edge
            scale_y = 0.8
        elif normalized_y > 0.9:  # Near bottom edge
            scale_y = 0.8
        else:
            scale_y = SCALING_FACTOR_Y  # Normal scaling in the center region

        # Scale the coordinates to enhance movement
        x = int(normalized_x * screen_width * scale_x)
        y = int(normalized_y * screen_height * scale_y)

        # Ensure that the scaled values do not exceed the screen size
        x = min(max(0, x), screen_width - 1)
        y = min(max(0, y), screen_height - 1)

        # Apply smoothing
        x, y = smooth_movement(x, y, prev_x, prev_y)

        if drawing_mode:
            try:
                pyautogui.dragTo(x, y, button='left')
            except FailSafeException:
                print("Fail-safe triggered during drag action.")
        else:
            move_mouse_safe(x, y)  # Using safe mouse move

        prev_x, prev_y = x, y


def detect_gestures(frame, landmarks_list, processed):
    global drawing_mode
    if len(landmarks_list) >= 21:
        index_finger_tip = find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmarks_list[4], landmarks_list[5]])

        # Check if the thumb and pinky finger tips are in contact for drawing mode
        if functions.is_thumb_pinky_touch(landmarks_list):
            drawing_mode = True
            cv2.putText(frame, "Drawing Mode On", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            drawing_mode = False
            #cv2.putText(frame, "Drawing Mode Off", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Close window gesture: thumb and ring finger tips touching
        if functions.is_close_window_gesture(landmarks_list):
            pyautogui.hotkey('alt', 'f4')  # Close the current window (use 'command', 'w' for macOS)
            cv2.putText(frame, "Window Closed", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Minimize window gesture: thumb and middle finger tips touching
        if functions.is_minimize_window_gesture(landmarks_list):
           pyautogui.hotkey('win', 'm')  # Directly minimize the current window (Windows)
           cv2.putText(frame, "Window Minimized", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)


        # Ensure that thumb and index fingers are NOT touching before performing other actions
        if not functions.is_thumb_index_touch(landmarks_list):
            # Perform regular mouse movement when thumb and index are NOT touching
            if thumb_index_dist < 50 and util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90:
                move_mouse(index_finger_tip)

            # Left Click
            elif functions.is_left_click(landmarks_list, thumb_index_dist):
                mouse.press(Button.left)
                mouse.release(Button.left)
                cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 0), 2)

            # Right Click
            elif functions.is_right_click(landmarks_list, thumb_index_dist):
                mouse.press(Button.right)
                mouse.release(Button.right)
                cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Double Click
            elif functions.is_double_click(landmarks_list, thumb_index_dist):
                pyautogui.doubleClick()
                cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Screenshot
            elif functions.is_screenshot(landmarks_list, thumb_index_dist):
                im1 = pyautogui.screenshot()
                label = random.randint(1, 1000)
                im1.save(f'my_screenshot_{label}.png')
                cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Scroll only if thumb and index are touching
        elif functions.is_scroll_up(landmarks_list):
            pyautogui.scroll(300)  # Adjust scroll speed as needed
            cv2.putText(frame, "Scroll Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Scroll Down
        elif functions.is_scroll_down(landmarks_list):
            pyautogui.scroll(-300)  # Adjust scroll speed as needed
            cv2.putText(frame, "Scroll Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)




        
def main():
    cap = cv2.VideoCapture(0)
    draw = mp.solutions.drawing_utils
    try:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            processed = hands.process(frameRGB)
            landmarks_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    landmarks_list.append((lm.x, lm.y))

            detect_gestures(frame, landmarks_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    