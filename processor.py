import cv2
from ultralytics import YOLO
from collections import deque
from utils import calculate_distance, draw_player, draw_ball, draw_trail, draw_possession

model = YOLO("yolov8n.pt")

ball_trail = deque(maxlen=30)

team_A_frames = 0
team_B_frames = 0
total_frames = 0


def process_frame(frame):
    global ball_trail, team_A_frames, team_B_frames, total_frames

    total_frames += 1

    results = model.track(frame, classes=[0,32], persist=True, verbose=False)

    players = []
    ball_center = None

    if results[0].boxes is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()

        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1+x2)//2, (y1+y2)//2

            if int(cls) == 0:
                players.append((cx, cy, x1, y1, x2, y2))
                draw_player(frame, (x1,y1,x2,y2))

            elif int(cls) == 32:
                ball_center = (cx, cy)
                ball_trail.append(ball_center)
                draw_ball(frame, (x1,y1,x2,y2))

    owner = None

    if ball_center and players:
        min_dist = float("inf")

        for p in players:
            dist = calculate_distance((p[0], p[1]), ball_center)

            if dist < min_dist:
                min_dist = dist
                owner = p

        if owner:
            px = owner[0]

            if px < frame.shape[1]//2:
                team_A_frames += 1
                color = (255,0,0)
            else:
                team_B_frames += 1
                color = (0,255,0)

            cv2.rectangle(frame, (owner[2], owner[3]), (owner[4], owner[5]), color, 3)

    draw_trail(frame, ball_trail)

    if total_frames > 0:
        A_pct = int((team_A_frames/total_frames)*100)
        B_pct = int((team_B_frames/total_frames)*100)

        draw_possession(frame, A_pct, B_pct)

    return frame