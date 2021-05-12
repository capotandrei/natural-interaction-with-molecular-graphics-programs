import cv2
import math
import numpy as np

from handDetector import HandDetector


class HandGestures:
    @staticmethod
    def fingers_count(queue):
        handDetector = HandDetector(min_detection_confidence=0.7)
        webcamFeed = cv2.VideoCapture(0)
        while True:
            status, image = webcamFeed.read()
            handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
            count = 0

            if len(handLandmarks) != 0:
                if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:  # Right Thumb
                    count = count + 1
                elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:  # Left Thumb
                    count = count + 1
                if handLandmarks[8][2] < handLandmarks[6][2]:  # Index finger
                    count = count + 1
                if handLandmarks[12][2] < handLandmarks[10][2]:  # Middle finger
                    count = count + 1
                if handLandmarks[16][2] < handLandmarks[14][2]:  # Ring finger
                    count = count + 1
                if handLandmarks[20][2] < handLandmarks[18][2]:  # Little finger
                    count = count + 1

            if count == 1:
                queue.put({'save': "molecule_1d86.mmod"})
            elif count == 2:
                queue.put({'rotate180right': 5})
            elif count == 3:
                queue.put({'rotate180left': -5})
            elif count == 4:
                queue.put({'rotateup': 5})
            elif count == 5:
                queue.put({'rotatedown': -5})

            cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
            cv2.imshow("Volume", image)
            cv2.waitKey(1)

    @staticmethod
    def zoom_controller(queue):
        handDetector = HandDetector(min_detection_confidence=0.7)
        webcamFeed = cv2.VideoCapture(0)
        while True:
            status, image = webcamFeed.read()
            handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
            volumeValue = 0
            if len(handLandmarks) != 0:
                x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
                x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
                length = math.hypot(x2 - x1, y2 - y1)

                volumeValue = np.interp(length, [50, 250], [-1, 1])  # coverting length to proportionate to volume range
                queue.put({'translate': [0, 0, volumeValue]})

                cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cv2.putText(image, 'Zoom ratio: ' + str(round(volumeValue, 2)),
                        (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            cv2.imshow("Zoom Flow", image)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        webcamFeed.release()
        cv2.destroyAllWindows()
