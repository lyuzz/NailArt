from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import mediapipe as mp
import cv2

from app.utils.errors import HandNotDetectedError


@dataclass
class HandResult:
    handedness: str
    landmarks: List[Tuple[int, int]]


def detect_hand(image_bgr: np.ndarray) -> HandResult:
    mp_hands = mp.solutions.hands
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5,
    ) as hands:
        rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        if not result.multi_hand_landmarks:
            raise HandNotDetectedError("No hand detected")

        hand_landmarks = result.multi_hand_landmarks
        handedness_list = result.multi_handedness or []
        selected_idx = 0
        if len(hand_landmarks) > 1:
            areas = []
            for idx, hand in enumerate(hand_landmarks):
                xs = [lm.x for lm in hand.landmark]
                ys = [lm.y for lm in hand.landmark]
                areas.append((max(xs) - min(xs)) * (max(ys) - min(ys)))
            selected_idx = int(np.argmax(areas))

        selected = hand_landmarks[selected_idx]
        handed = "Unknown"
        if handedness_list:
            handed = handedness_list[selected_idx].classification[0].label

        h, w = image_bgr.shape[:2]
        landmarks_px = []
        for lm in selected.landmark:
            landmarks_px.append((int(lm.x * w), int(lm.y * h)))
        return HandResult(handedness=handed, landmarks=landmarks_px)
