import copy
import itertools
import keyboard
import mouse
import cv2 as cv
import numpy as np
import mediapipe as mp
from utils import CvFpsCalc
import pygame
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
pyautogui.FAILSAFE = False

pygame.mixer.init()

def main():
    cap_device, cap_width, cap_height = 0, 1920, 1080
    min_detection_confidence, min_tracking_confidence = 0.7, 0.5
    use_brect = True
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    cvFpsCalc = CvFpsCalc(buffer_len=10)

    previousIndexY, previousIndexX = 0, 0
    thumbX, thumbY = 0, 0
    previousClick, currentClick = False, False
    clickCounter, scrollStarting, previousScroll,scrollCounter = 0, 0, 0,0
    running = True
    toggle_pressed = False
    arrowCounter = 0
    mouseAction = "none"
    volumeOn = False
    pressed = False
    previousVolume = False
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    while True:
        fps = cvFpsCalc.get()
        key = cv.waitKey(1)
        
        if key == 27:
            break

        if keyboard.is_pressed('t'):
            if not toggle_pressed:
                running = not running
                toggle_pressed = True
        else:
            toggle_pressed = False

        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)
        debug_image = copy.deepcopy(image)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                brect = calc_bounding_rect(debug_image, hand_landmarks)
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)

                indexFingerX, indexFingerY = landmark_list[8]
                middleFingerX, middleFingerY = landmark_list[12]
                ringFingerX,ringFingerY = landmark_list[16]
                pinkyFingerX,pinkyFingerY = landmark_list[20]
                thumbX, thumbY = landmark_list[4]
                wristX, wristY = landmark_list[0]

                # CLEAN LATER
                """if ((abs(indexFingerX - thumbX) < 20 and abs(indexFingerY - thumbY) < 20) and (abs(middleFingerX - thumbX) < 20 and abs(middleFingerY - thumbY) < 20) and (abs(middleFingerX - thumbX) < 20 and abs(middleFingerY - thumbY) < 20) and (abs(pinkyFingerX - thumbX) < 20 and abs(pinkyFingerY - thumbY) < 20)):
                    run = not run
        
                if run==False and previousRun!=run:
                    running = not running
                    pygame.mixer.Sound('./assets/ding.wav').play()


                previousRun = run"""

                if running:
                    if abs(indexFingerX - thumbX) < 30 and abs(indexFingerY - thumbY) < 30:
                        currentClick=True
                        if clickCounter<50:
                            clickCounter+=1
                    else:
                        currentClick=False
                        clickCounter, scrollStarting, previousScroll = 0, 0, 0

                    if previousClick != currentClick and currentClick: mouse.click(button='left')

                    if clickCounter>6:
                        scrollStarting = (indexFingerY + thumbY)/2
                        if clickCounter<9: previousScroll = scrollStarting
                        mouse.wheel((scrollStarting - previousScroll)/20)
                    
                    previousClick = currentClick
                    previousScroll = scrollStarting
                    if thumbY<wristY  and thumbY>landmark_list[6][1] and abs(landmark_list[6][1]-landmark_list[5][1])<40 and abs(landmark_list[10][1]-landmark_list[9][1])<40 and abs(landmark_list[14][1]-landmark_list[13][1])<40 and abs(landmark_list[17][1]-landmark_list[18][1])<40 and (indexFingerY>landmark_list[5][1]):
                        if thumbX>landmark_list[3][0] and landmark_list[2][0] >wristX:
                            arrowCounter +=1
                            if arrowCounter>16:
                                keyboard.press_and_release("right")
                                arrowCounter=0

                        elif thumbX<landmark_list[3][0] and landmark_list[2][0] <wristX:
                            arrowCounter+=1
                            if arrowCounter>16:
                                keyboard.press_and_release("left")
                                arrowCounter=0
                        else:
                            arrowCounter = 9
                    else: 
                        arrowCounter = 9

                    '''if abs(indexFingerX - previousIndexX)<3:
                        indexFingerX = previousIndexX
                    
                    if abs(indexFingerY - previousIndexY)<3:
                        indexFingerY = previousIndexY'''
                    
                    if (abs(ringFingerX - middleFingerX) < 30 and abs(ringFingerY - middleFingerY) < 30) and (pinkyFingerY<landmark_list[19][1]) and (indexFingerY<landmark_list[7][1]):
                        volumeOn = True
                        
                    else:
                        volumeOn=False

                    if volumeOn == True and previousVolume!=volumeOn:

                        volumeStarting = thumbY

                    if volumeOn:

                        if thumbY>volumeStarting+30:
                            pyautogui.press("volumedown")
                        if thumbY<volumeStarting-30:
                            pyautogui.press("volumeup")
                            

                        
                   
                    mouse.move(((indexFingerX+thumbX)/2)*2, ((indexFingerY+thumbY)/2)*2, absolute=True)

                    previousVolume=volumeOn
                    
                debug_image = draw_bounding_rect(use_brect, debug_image, brect)
                debug_image = draw_info_text(debug_image, brect)

        debug_image = draw_info(debug_image, fps)
        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()

def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point = [np.array((landmark_x, landmark_y))]
        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)
    return [x, y, x + w, y + h]
    
def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]
    landmark_point = []

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        landmark_point.append([landmark_x, landmark_y])
    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]
        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))
    return temp_landmark_list

def draw_bounding_rect(use_brect, image, brect):
    if use_brect: cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 0, 0), 1)
    return image

def draw_info_text(image, brect):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22), (0, 0, 0), -1)
    cv.putText(image, "PLACEHOLDER", (brect[0] + 5, brect[1] - 4), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
    return image

def draw_info(image, fps):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv.LINE_AA)
    return image

if __name__ == '__main__':
    main()