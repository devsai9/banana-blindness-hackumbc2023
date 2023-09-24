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

pyautogui.FAILSAFE = False

pygame.mixer.init()



def ArraytoHandMap(landmark_list):


    thumb = {
        'one':{'x':landmark_list[1][0], 'y':landmark_list[1][1]},
        'two':{'x':landmark_list[2][0], 'y':landmark_list[2][1]},
        'three':{'x':landmark_list[3][0], 'y':landmark_list[3][1]},
        'four':{'x':landmark_list[4][0], 'y':landmark_list[4][1]},
    }
    index = {
        'one':{'x':landmark_list[5][0], 'y':landmark_list[5][1]},
        'two':{'x':landmark_list[6][0], 'y':landmark_list[6][1]},
        'three':{'x':landmark_list[7][0], 'y':landmark_list[7][1]},
        'four':{'x':landmark_list[8][0], 'y':landmark_list[8][1]},
    }

    middle ={
        'one':{'x':landmark_list[9][0], 'y':landmark_list[9][1]},
        'two':{'x':landmark_list[10][0], 'y':landmark_list[10][1]},
        'three':{'x':landmark_list[11][0], 'y':landmark_list[11][1]},
        'four':{'x':landmark_list[12][0], 'y':landmark_list[12][1]},
    }
    ring = {
        'one':{'x':landmark_list[13][0], 'y':landmark_list[13][1]},
        'two':{'x':landmark_list[14][0], 'y':landmark_list[14][1]},
        'three':{'x':landmark_list[15][0], 'y':landmark_list[15][1]},
        'four':{'x':landmark_list[16][0], 'y':landmark_list[16][1]},
    }
    pinky = {
        'one':{'x':landmark_list[17][0], 'y':landmark_list[17][1]},
        'two':{'x':landmark_list[18][0], 'y':landmark_list[18][1]},
        'three':{'x':landmark_list[19][0], 'y':landmark_list[19][1]},
        'four':{'x':landmark_list[20][0], 'y':landmark_list[20][1]},
    }
    wrist = {
        'one':{'x':landmark_list[0][0],'y':landmark_list[0][1]}
    }

    hand = {'thumb':thumb,'index':index,'middle':middle,'ring':ring,'pinky':pinky, 'wrist':wrist}

    return hand


def currentCursorMode(handMap):

    errVar = 40

    currentCursor = "none"

    if abs(handMap['thumb']['four']['x'] - handMap['index']['four']['x'])<errVar and abs(handMap['index']['four']['y'] - handMap['thumb']['four']['y'])<errVar:

        if handMap['ring']['four']['y']>handMap['thumb']['three']['y'] and handMap['pinky']['four']['y']>handMap['thumb']['three']['y']:

            if handMap['middle']['four']['y']>handMap['thumb']['three']['y']:
                currentCursor = "pointer"

            elif handMap['middle']['four']['y']<handMap['thumb']['three']['y']:
                currentCursor = "drag"


    elif handMap['thumb']['four']['y'] < handMap['wrist']['one']['y'] and handMap['thumb']['four']['y']>handMap['index']['two']['y']:

        if handMap['index']['four']['y']>handMap['thumb']['three']['y'] and handMap['pinky']['four']['y']>handMap['thumb']['three']['y']:
            if handMap['middle']['four']['y']>handMap['thumb']['three']['y'] and handMap['ring']['four']['y']>handMap['thumb']['three']['y']:
                
                    

                        if handMap['thumb']['four']['x']>handMap['thumb']['three']['x'] and handMap['thumb']['two']['x']>handMap['wrist']['one']['x']:

                            currentCursor = "rightarrow"

                        elif handMap['thumb']['four']['x']<handMap['thumb']['three']['x'] and handMap['thumb']['two']['x']<handMap['wrist']['one']['x']:

                            currentCursor = "leftarrow"

    elif (abs(handMap['middle']['four']['x'] - handMap['thumb']['four']['x']) < errVar and abs(handMap['middle']['four']['y'] - handMap['thumb']['four']['y']) < errVar):

         if (abs(handMap['ring']['four']['x'] - handMap['thumb']['four']['x']) < errVar and abs(handMap['ring']['four']['y'] - handMap['thumb']['four']['y']) < errVar):

            if(abs(handMap['index']['four']['y'] < handMap['middle']['four']['y']) and abs(handMap['pinky']['four']['y']< handMap['ring']['four']['y']) ):
                currentCursor='volume'

    elif handMap['ring']['four']['y']<handMap['index']['two']['y'] and handMap['pinky']['four']['y']<handMap['index']['two']['y']:
        currentCursor="cursor"

    else:
        currentCursor="none"

                        
                        

        

        
        
        
       
    return currentCursor
    





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

    cvFpsCalc = CvFpsCalc(buffer_len=12)

    previousIndexY, previousIndexX = 0, 0
    
    previousClick, currentClick = False, False
    clickCounter, scrollStarting, previousScroll,scrollCounter = 0, 0, 0,0
    running = True
    toggle_pressed = False
    arrowCounter = 0
    previousCursor = ""
   
    pressed = False
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

                handMap = ArraytoHandMap(landmark_list)



               

               
                currentCursor = ""
                previousVolume = False
                volumeOn = False
                # CLEAN LATER
                """if ((abs(handMap['index']['four']['x'] - handMap['thumb']['four']['x']) < 20 and abs(handMap['index']['four']['y'] - handMap['thumb']['four']['y']) < 20) and (abs(ringFingerX - handMap['thumb']['four']['x']) < 20 and abs(ringFingerY - handMap['thumb']['four']['y']) < 20) and (abs(middleFingerX - handMap['thumb']['four']['x']) < 20 and abs(middleFingerY - handMap['thumb']['four']['y']) < 20) and (abs(pinkyFingerX - handMap['thumb']['four']['x']) < 20 and abs(pinkyFingerY - handMap['thumb']['four']['y']) < 20)):
                    run = not run
        
                if run==False and previousRun!=run:
                    running = not running
                    pygame.mixer.Sound('./assets/ding.wav').play()


                previousRun = run"""

                if running:
                  
                    currentCursor = currentCursorMode(handMap)
                    #print(currentCursor)
                    if currentCursor == "pointer":
                        currentClick=True
                        if clickCounter<50:
                            clickCounter+=1
                    else:
                        currentClick=False
                        clickCounter, scrollStarting, previousScroll = 0, 0, 0

                    if previousClick != currentClick and currentClick: mouse.click(button='left')

                    if clickCounter>6:
                        scrollStarting = (handMap['index']['four']['y'] + handMap['thumb']['four']['y'])/2
                        if clickCounter<9: previousScroll = scrollStarting
                        mouse.wheel((scrollStarting - previousScroll)/20)
                    
                    previousClick = currentClick
                    previousScroll = scrollStarting

                    if currentCursor == "drag" and previousCursor!="drag":

                       mouse.press()

                    if previousCursor=="drag" and currentCursor!="drag":
                        mouse.release(button='left')

                    
                    
                    
                    if currentCursor=="rightarrow":
                        arrowCounter+=1

                        if arrowCounter>14:
                            keyboard.press_and_release("right")
                            arrowCounter=0

                    elif currentCursor =="leftarrow":
                        arrowCounter+=1
                        if arrowCounter>14:
                            keyboard.press_and_release("left")
                            arrowCounter=0

                    if currentCursor!='leftarrow' and currentCursor!="rightarrow":
                        arrowCounter=9

                  

               



                    

        

                    if abs(handMap['index']['four']['x'] - previousIndexX)<6:
                        handMap['index']['four']['x'] = previousIndexX
                    
                    if abs(handMap['index']['four']['y'] - previousIndexY)<6:
                        handMap['index']['four']['y'] = previousIndexY
                    
                    if currentCursor=='volume':
                        volumeOn = True
                    else:
                        volumeOn=False

                    if volumeOn == True and previousVolume!=volumeOn:
                        volumeStarting = handMap['thumb']['four']['y']

                    '''if volumeOn:
                        if handMap['thumb']['four']['y']>volumeStarting+30:
                            keyboard.press("volumedown")
                        if handMap['thumb']['four']['y']<volumeStarting-30:
                            keyboard.press("fn+f2")'''

                    previousVolume = volumeOn
                    previousCursor=currentCursor
                    
                    
                    mouse.move(((handMap['index']['four']['x']+handMap['thumb']['four']['x'])/2)*2, ((handMap['index']['four']['y']+handMap['thumb']['four']['y'])/2)*2, absolute=True)
                    
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