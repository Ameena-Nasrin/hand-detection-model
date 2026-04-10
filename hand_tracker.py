import cv2
import mediapipe as mp
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.85, track_con=0.5):
        self.detection_available = False
        try:
            # Try to use new MediaPipe Tasks API
            model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
            if not os.path.exists(model_path):
                print("Warning: hand_landmarker.task model file not found")
                self.detection_available = False
            else:
                base_options = python.BaseOptions(model_asset_path=model_path)
                options = vision.HandLandmarkerOptions(
                    base_options=base_options,
                    num_hands=max_hands,
                    min_hand_detection_confidence=detection_con,
                    min_hand_presence_confidence=track_con,
                    min_tracking_confidence=track_con
                )
                self.landmarker = vision.HandLandmarker.create_from_options(options)
                self.mp_draw = mp.tasks.vision.drawing_utils
                self.detection_available = True
        except Exception as e:
            print(f"Warning: MediaPipe hand detection not available: {e}")
            self.detection_available = False

        self.tip_ids = [4, 8, 12, 16, 20]  # Hand landmark indices for fingertips

    def find_hands(self, img, draw=True):
        if not self.detection_available:
            # Mock implementation - just return the image
            self.results = None
            return img

        # Convert BGR to RGB for MediaPipe
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to MediaPipe Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

        # Detect hands
        self.results = self.landmarker.detect(mp_image)

        if draw and self.results.hand_landmarks:
            h, w, c = img.shape
            for hand_landmarks in self.results.hand_landmarks:
                # Draw landmarks and connections manually
                landmarks = hand_landmarks
                
                # Draw connections
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
                    (0, 5), (5, 6), (6, 7), (7, 8),  # Index
                    (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
                    (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
                    (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
                    (5, 9), (9, 13), (13, 17)  # Palm connections
                ]
                
                for connection in connections:
                    p1 = landmarks[connection[0]]
                    p2 = landmarks[connection[1]]
                    x1, y1 = int(p1.x * w), int(p1.y * h)
                    x2, y2 = int(p2.x * w), int(p2.y * h)
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw landmarks
                for landmark in landmarks:
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(img, (x, y), 5, (255, 0, 0), -1)
                    
        return img

    def find_position(self, img):
        if not self.detection_available:
            # Mock implementation - return empty list
            self.lm_list = []
            return self.lm_list

        self.lm_list = []
        if self.results and self.results.hand_landmarks:
            # Get the first detected hand
            hand_landmarks = self.results.hand_landmarks[0]
            h, w, c = img.shape
            for id, landmark in enumerate(hand_landmarks):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                self.lm_list.append([id, cx, cy])
        return self.lm_list

    def fingers_up(self):
        if not self.detection_available or not self.lm_list:
            # Mock implementation - return all fingers down
            return [0, 0, 0, 0, 0]

        fingers = []

        # Thumb (check if tip is to the left/right of joint)
        if self.lm_list[self.tip_ids[0]][1] < self.lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers (Check if tip is above joint)
        for id in range(1, 5):
            if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers