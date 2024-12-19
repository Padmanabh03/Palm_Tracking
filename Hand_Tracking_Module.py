import cv2
import mediapipe as mp
import time
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class HandTracker:
    def __init__(self,mode = False, max_hands=2, detection_confidence=0.75, tracking_confidence=0.5):
        self.mode = mode
        self.video = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_hands,
                                         min_detection_confidence=detection_confidence,
                                         min_tracking_confidence=tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.previous_time = 0

    def process_frame(self, frame,draw =True):
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(rgb_img)

        if self.result.multi_hand_landmarks:
            for hand_landmark in self.result.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame,hand_landmark,self.mp_hands.HAND_CONNECTIONS)

        return frame

    def get_landmarks(self, frame):
        # Extracts landmarks from the frame and returns a list of their positions.
        landmark_list = []
        if self.result.multi_hand_landmarks:
            for hand_landmark in self.result.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmark.landmark):
                    height, width, channel = frame.shape
                    cx, cy = int(lm.x * width), int(lm.y * height)
                    landmark_list.append([id, cx, cy])
                    # print(f"Landmark ID: {id}, X: {cx}, Y: {cy}")  # Print each landmark's coordinates
        return landmark_list


    def calculate_fps(self):
        current_time = time.time()
        fps = 1 / (current_time - self.previous_time)
        self.previous_time = current_time
        return fps

    def release(self):
        self.video.release()
        cv2.destroyAllWindows()

    def set_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)
        # self.volume.GetMute()
        # self.volume.GetMasterVolumeLevel()
        volume_range = self.volume.GetVolumeRange()
        #sself.volume.SetMasterVolumeLevel(-20.0, None)  # Corrected this line
        min_volume = volume_range[0]
        max_volume = volume_range[1]
        return min_volume,max_volume

        




    def run(self):
        while True:
            ret, frame = self.video.read()
            if not ret:
                print("Failed to capture video. Exiting...")
                break

            result_frame = self.process_frame(frame)
            landmark_list = self.get_landmarks(result_frame)
            min_vol,max_vol = self.set_volume()
            vol_bar = 400
            vol_per = 0

            

            if len(landmark_list)!=0:
                # print(landmark_list[4],landmark_list[8])

                x1,y1 = landmark_list[4][1], landmark_list[4][2]
                x2,y2 = landmark_list[8][1], landmark_list[8][2]
                cx,cy = (x1+x2)//2,(y1+y2)//2

                cv2.circle(frame,(x1,y1),15,(225,0,0),cv2.FILLED)
                cv2.circle(frame,(x2,y2),15,(225,0,0),cv2.FILLED)
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,255),3)
                cv2.circle(frame,(cx,cy),15,(0,255,0),cv2.FILLED)

                length = math.hypot(x2-x1,y2-y1)
                vol = np.interp(length,[50,200],[min_vol,max_vol])
                vol_bar = np.interp(length,[50,200],[400,150])
                vol_per = np.interp(length,[50,200],[0,100])
                self.volume.SetMasterVolumeLevel(vol, None)



                if length < 50:
                    cv2.circle(frame,(cx,cy),15,(0,0,255),cv2.FILLED)

            cv2.rectangle(frame,(50,150),(85,400),(0,255,0),3)
            cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, str(int(vol_per))+'%' , (40, 450), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 255), 2)



            fps = self.calculate_fps()
            cv2.putText(result_frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 0), 3)

            resize_frame = cv2.resize(result_frame, (1080, 720))
            self.display_frame(resize_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.release()

    def display_frame(self, frame):
        # Displays the given frame in a window.
        cv2.imshow('Frame', frame)

    def __del__(self):
        # Destructor to ensure resources are released.
        self.release()

if __name__ == "__main__":
    hand_tracker = HandTracker()
    hand_tracker.run()
