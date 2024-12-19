import cv2
import mediapipe as mp
import time

video = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

currentTime = 0
previousTime = 0

while True:

    ret, frame = video.read()

    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_img)

    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmark.landmark):
                height, width, channel = frame.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                print(id, cx, cy)
                if id == 0:
                    cv2.circle(frame, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime

    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 255, 0), 3)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
video.release()
# Destroy all the windows
cv2.destroyAllWindows()
