import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import webbrowser

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# open the website on the browser
url = 'https://pagegabut.000webhostapp.com/pagelogin/landingpage.php'
webbrowser.get().open(url)

cap = cv2.VideoCapture(0)
screen_size = pyautogui.size()

def close_hand_action(hand_landmarks):
    # Dapatkan posisi jari telunjuk pada landmark tangan
    index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    # Konversi posisi landmark menjadi posisi pixel pada layar
    screen_x = int(index_finger_x * screen_size.width)
    screen_y = int(index_finger_y * screen_size.height)
    # Gerakkan cursor ke posisi pixel tersebut
    pyautogui.moveTo(screen_x, screen_y)

# set min detection confidence and min tracking confidence to 0.8
with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8) as hands:
    while True :
        _,frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        image.flags.writeable = False
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # get the x and y coordinates of the tip of index finger
                index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                # scroll up or down based on the position of index finger
                if index_finger_y < 0.2:
                    pyautogui.scroll(-1)
                elif index_finger_y > 0.8:
                    pyautogui.scroll(1)
                    time.sleep(0.2) 
                    # wait for 0.2 seconds before another scroll action
                # move the cursor based on the position of index finger
                screen_width, screen_height = pyautogui.size()
                button_x = int(index_finger_x * screen_width)
                button_y = int(index_finger_y * screen_height)

                # click the button on the website
                pyautogui.click(x=button_x, y=button_y)

                # simulate a click action if the thumb is up
                thumb_is_up = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
                if thumb_is_up:
                    pyautogui.click()
                    time.sleep(0.5) # wait for 0.5 seconds before another click action
        
        cv2.imshow('Hand Tracking', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()

cv2.destroyAllWindows()
