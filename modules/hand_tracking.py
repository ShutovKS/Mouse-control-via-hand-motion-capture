import time

import cv2
import mediapipe as mp


class HandTracking:
    def __init__(self):
        self.results = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
        self.hand_gestures = HandGestures()
        self.fist = False
        self.palm = False
        self.fist_start_time = None
        self.palm_start_time = None
        self.gesture_duration_threshold = 0.1

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_hand_coordinates(self, frame):
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    return cx, cy
        return None, None

    def detect_hand_gestures(self, frame):
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.hand_gestures.fist = self.is_fist(hand_landmarks)
                self.hand_gestures.palm = self.is_palm(hand_landmarks)
        return self.hand_gestures

    def is_fist(self, hand_landmarks):
        """
        Проверяет, является ли жест кулаком.
        Жест кулака определяется, если все пальцы согнуты. Для этого кончики пальцев должны быть ближе к ладони.
        """
        landmarks = hand_landmarks.landmark
        finger_tips = [self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                       self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                       self.mp_hands.HandLandmark.RING_FINGER_TIP,
                       self.mp_hands.HandLandmark.PINKY_TIP]

        for tip in finger_tips:
            if landmarks[tip].y < landmarks[tip - 2].y:  # Проверка, что кончик пальца выше среднего сустава
                self.fist = False
                self.fist_start_time = None
                return False

        current_time = time.time()
        if self.fist_start_time is None:
            self.fist_start_time = current_time

        if (current_time - self.fist_start_time) > self.gesture_duration_threshold:
            self.fist = True
            return True
        return False

    def is_palm(self, hand_landmarks):
        """
        Проверяет, является ли жест ладонью.
        Жест ладони определяется, если все пальцы выпрямлены. Для этого кончики пальцев должны быть выше или 
        на одном уровне с соответствующими суставами.
        """
        landmarks = hand_landmarks.landmark
        finger_tips = [self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                       self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                       self.mp_hands.HandLandmark.RING_FINGER_TIP,
                       self.mp_hands.HandLandmark.PINKY_TIP]

        for tip in finger_tips:
            if landmarks[tip].y > landmarks[tip - 2].y:  # Проверка, что кончик пальца выше среднего сустава
                self.palm = False
                self.palm_start_time = None
                return False

        current_time = time.time()
        if self.palm_start_time is None:
            self.palm_start_time = current_time

        if (current_time - self.palm_start_time) > self.gesture_duration_threshold:
            self.palm = True
            return True
        return False


class HandGestures:
    def __init__(self):
        self.fist = False
        self.palm = False
