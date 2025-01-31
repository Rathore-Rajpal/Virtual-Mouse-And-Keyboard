import virtualMouse
import cv2
import mediapipe as mp
import pyautogui
from pynput.mouse import Button, Controller
import random
import functions
import util
from pyautogui import FailSafeException

def detect_gestures(frame, landmarks_list, processed):
    global drawing_mode
    if len(landmarks_list) >= 21:
        index_finger_tip = virtualMouse.find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmarks_list[4], landmarks_list[5]])

        # Check if the thumb and pinky finger tips are in contact for drawing mode
        if functions.is_thumb_pinky_touch(landmarks_list):
            drawing_mode = True
            cv2.putText(frame, "Drawing Mode On", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            drawing_mode = False
            cv2.putText(frame, "Drawing Mode Off", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

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
                virtualMouse.move_mouse(index_finger_tip)

            # Left Click
            elif functions.is_left_click(landmarks_list, thumb_index_dist):
                virtualMouse.mouse.press(Button.left)
                virtualMouse.mouse.release(Button.left)
                cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 0), 2)

            # Right Click
            elif functions.is_right_click(landmarks_list, thumb_index_dist):
                virtualMouse.mouse.press(Button.right)
                virtualMouse.mouse.release(Button.right)
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
