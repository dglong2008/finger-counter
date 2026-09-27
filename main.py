import math

import cv2
import mediapipe as mp

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def angle(a, b, c):
    """Tinh goc ABC tu 3 landmark."""
    angle1 = math.atan2(a.y - b.y, a.x - b.x)
    angle2 = math.atan2(c.y - b.y, c.x - b.x)
    value = abs(math.degrees(angle1 - angle2))
    return min(value, 360 - value)


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


# Finger counting logic
def count_fingers(hand_landmarks):
    lm = hand_landmarks.landmark
    count = 0

    # Thumb
    if (
        angle(lm[2], lm[3], lm[4]) > 150
        and distance(lm[4], lm[5]) > distance(lm[3], lm[5])
    ):
        count += 1

    # Other four fingers
    fingers = [(5, 6, 8), (9, 10, 12), (13, 14, 16), (17, 18, 20)]
    for mcp, pip, tip in fingers:
        if angle(lm[mcp], lm[pip], lm[tip]) > 160:
            count += 1

    return count


# Camera loop
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Khong mo duoc camera. Hay kiem tra quyen camera hoac camera index.")
        return

    with mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)
            total_fingers = 0

            if result.multi_hand_landmarks and result.multi_handedness:
                for hand_landmarks, handedness in zip(
                    result.multi_hand_landmarks, result.multi_handedness
                ):
                    finger_count = count_fingers(hand_landmarks)
                    total_fingers += finger_count
                    hand_label = handedness.classification[0].label

                    mp_draw.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    h, w, _ = frame.shape
                    wrist = hand_landmarks.landmark[0]
                    x = int(wrist.x * w)
                    y = int(wrist.y * h) - 20
                    cv2.putText(
                        frame,
                        f"{hand_label}: {finger_count}",
                        (x, max(y, 30)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                    )

            cv2.rectangle(frame, (10, 10), (230, 85), (0, 0, 0), -1)
            cv2.putText(
                frame,
                f"TOTAL: {total_fingers}",
                (25, 58),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                "Press Q to quit",
                (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Finger Counter", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
