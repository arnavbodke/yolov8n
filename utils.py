import cv2
import numpy as np

def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def draw_player(frame, box, color=(255,255,255), thickness=1):
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)


def draw_ball(frame, box):
    x1, y1, x2, y2 = box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 2)


def draw_trail(frame, trail):
    for i in range(1, len(trail)):
        cv2.line(frame, trail[i-1], trail[i], (255,255,0), 2)


def draw_possession(frame, A_pct, B_pct):
    cv2.rectangle(frame, (10,10), (320,70), (0,0,0), -1)

    cv2.putText(frame, f"A: {A_pct}%", (20,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.putText(frame, f"B: {B_pct}%", (170,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)