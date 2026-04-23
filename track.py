import cv2
import numpy as np
import time
import math
import streamlit as st
from cvzone.HandTrackingModule import HandDetector

st.title("Air Canvas ")

run = st.checkbox("Start Camera")
FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

canvas = None
prev_x, prev_y = 0, 0

current_color = (255, 0, 255)
mode = "DRAW"

brush_thickness = 6
eraser_thickness = 30

#   Colors
colors = [
    ((255, 0, 255), "PINK"),
    ((255, 0, 0), "BLUE"),
    ((0, 255, 0), "GREEN"),
    ((255,255,0),"YELLOW"),
    ((0, 0, 255), "RED"),
    ((139, 69, 19), "BROWN"),
    ((0, 0, 0), "BLACK"),
    ((255, 255, 255), "CLEAR"),
]

angle_offset = 0

#   Mode control
app_mode = "HOME"

draw_hand_type = "Right"
ui_hand_type = "Left"

hover_start = 0
hover_choice = None


#   Color wheel
def draw_color_wheel(frame, cx, cy, angle_offset):
    radius = 100
    selected_index = None

    for i, (color, label) in enumerate(colors):
        angle = (i * (360 / len(colors)) + angle_offset) * math.pi / 180

        x = int(cx + radius * math.cos(angle))
        y = int(cy + radius * math.sin(angle))

        cv2.circle(frame, (x, y), 20, color, -1)

        if abs(y - (cy - radius)) < 25:
            cv2.circle(frame, (x, y), 28, (0,255,0), 2)
            selected_index = i

    return frame, selected_index


#   HOME UI
def draw_home_ui(frame):
    options = ["Draw: Left", "Draw: Right", "Start"]
    zones = []

    for i, text in enumerate(options):
        x1 = 50
        y1 = 100 + i * 80
        x2 = 300
        y2 = y1 + 50

        cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2)
        cv2.putText(frame, text, (x1+10, y1+30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        zones.append((x1,y1,x2,y2,text))

    return frame, zones


while run:
    success, frame = cap.read()
    if not success:
        st.write("Camera not working")
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.ones_like(frame) * 0

    hands, frame = detector.findHands(frame)

    left_hand, right_hand = None, None

    if hands:
        for hand in hands:
            if hand["type"] == "Left":
                right_hand = hand
            else:
                left_hand = hand

    # =====================   HOME MODE =====================
    if app_mode == "HOME":
        frame, zones = draw_home_ui(frame)

        if right_hand:
            lm = right_hand["lmList"]
            x, y = lm[8][0], lm[8][1]

            fingers = detector.fingersUp(right_hand)

            current_hover = None

            for (x1,y1,x2,y2,text) in zones:
                if x1 < x < x2 and y1 < y < y2:
                    current_hover = text
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)

            if fingers[1] == 1 and fingers[2] == 1:
                if current_hover == hover_choice:
                    if time.time() - hover_start > 0.7:
                        if current_hover == "Draw: Left":
                            draw_hand_type = "Left"
                            ui_hand_type = "Right"
                        elif current_hover == "Draw: Right":
                            draw_hand_type = "Right"
                            ui_hand_type = "Left"
                        elif current_hover == "Start":
                            app_mode = "DRAW"

                else:
                    hover_choice = current_hover
                    hover_start = time.time()

    # =====================  DRAW MODE =====================
    else:

        ui_hand = left_hand if ui_hand_type == "Left" else right_hand
        draw_hand = left_hand if draw_hand_type == "Left" else right_hand

        #   UI HAND
        if ui_hand:
            lm = ui_hand["lmList"]
            lx, ly = lm[8][0], lm[8][1]

            fingers = detector.fingersUp(ui_hand)

            if fingers[1] == 1 and fingers[2] == 0:
                angle_offset += 4

            frame, selected_index = draw_color_wheel(frame, lx, ly, angle_offset)

            if fingers[1] == 1 and fingers[2] == 1:
                if selected_index is not None:
                    selected_color = colors[selected_index][0]
                    label = colors[selected_index][1]

                    if label == "CLEAR":
                        canvas = np.ones_like(frame) * 0
                    elif label == "BLACK":
                        mode = "ERASE"
                    else:
                        mode = "DRAW"
                        current_color = selected_color

        #   DRAW HAND
        if draw_hand:
            lm = draw_hand["lmList"]
            rx, ry = lm[8][0], lm[8][1]

            fingers = detector.fingersUp(draw_hand)

            if fingers[1] == 1 and fingers[2] == 0:

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = rx, ry

                rx = int(prev_x * 0.5 + rx * 0.5)
                ry = int(prev_y * 0.5 + ry * 0.5)

                if mode == "DRAW":
                    cv2.line(canvas, (prev_x, prev_y), (rx, ry),
                             current_color, brush_thickness)
                else:
                    cv2.line(canvas, (prev_x, prev_y), (rx, ry),
                             (0,0,0), eraser_thickness)

                prev_x, prev_y = rx, ry

            else:
                prev_x, prev_y = 0, 0

        frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)

cap.release()