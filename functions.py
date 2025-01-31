import util

def is_left_click(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and 
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and
            thumb_index_dist > 50)

def is_right_click(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and 
            util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) > 90 and
            thumb_index_dist > 50)

def is_double_click(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and 
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_index_dist > 50)

def is_screenshot(landmarks_list, thumb_index_dist):
    return (util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8]) < 50 and 
            util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and
            thumb_index_dist < 50)

def is_thumb_pinky_touch(landmarks_list):
    # Gesture: Thumb tip (landmarks_list[4]) touching Pinky finger tip (landmarks_list[20])
    return util.get_distance([landmarks_list[4], landmarks_list[20]]) < 30  # Adjust threshold as needed

def is_thumb_index_touch(landmarks_list):
    # Gesture: Thumb tip (landmarks_list[4]) touching Index finger tip (landmarks_list[8])
    return util.get_distance([landmarks_list[4], landmarks_list[8]]) < 30  # Adjust threshold as needed

def is_scroll_up(landmarks_list):
    # Gesture: Scroll up only if the thumb and index fingers are touching and index finger moves upwards
    if is_thumb_index_touch(landmarks_list):  # Ensure thumb and index are touching
        return landmarks_list[8][1] < landmarks_list[7][1]  # Tip of the index finger above the middle of the finger
    return False

def is_scroll_down(landmarks_list):
    # Gesture: Scroll down only if the thumb and index fingers are touching and index finger moves downwards
    if is_thumb_index_touch(landmarks_list):  # Ensure thumb and index are touching
        return landmarks_list[8][1] > landmarks_list[7][1]  # Tip of the index finger below the middle of the finger
    return False

def is_close_window_gesture(landmarks_list):
    # Gesture: Thumb tip (landmarks_list[4]) touching Ring finger tip (landmarks_list[16])
    return util.get_distance([landmarks_list[4], landmarks_list[16]]) < 30  # Adjust the threshold as needed

def is_minimize_window_gesture(landmarks_list):
    # Gesture: Thumb tip (landmarks_list[4]) touching Middle finger tip (landmarks_list[12])
    return util.get_distance([landmarks_list[4], landmarks_list[12]]) < 30  # Adjust the threshold as needed

