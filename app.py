import cv2
import numpy as np
import hand_tracker as ht

 
canvas_width, canvas_height = 1280, 720
draw_color = (255, 0, 255)  
brush_thickness = 15
eraser_thickness = 80
xp, yp = 0, 0  

 
img_canvas = np.zeros((canvas_height, canvas_width, 3), np.uint8)

cap = cv2.VideoCapture(0)
cap.set(3, canvas_width)
cap.set(4, canvas_height)

detector = ht.HandDetector(detection_con=0.85)

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Failed to capture image from camera")
        break
    
    img = cv2.flip(img, 1)  

     
    img = detector.find_hands(img)
    lm_list = detector.find_position(img)

    if len(lm_list) != 0:
         
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]

         
        fingers = detector.fingers_up()

         
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0 # Reset drawing path
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)
            
           
            if y1 < 100:
                if 250 < x1 < 450: # Red zone
                    draw_color = (0, 0, 255)
                elif 550 < x1 < 750: # Green zone
                    draw_color = (0, 255, 0)
                elif 850 < x1 < 1050: # Eraser zone
                    draw_color = (0, 0, 0)

       
        if fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)
            
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if draw_color == (0, 0, 0): # Eraser mode
                cv2.line(img, (xp, yp), (x1, y1), draw_color, eraser_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, eraser_thickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), draw_color, brush_thickness)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)
            
            xp, yp = x1, y1

   
    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    
    # Ensure images have the same size before bitwise operations
    if img.shape == img_inv.shape and img.shape == img_canvas.shape:
        img = cv2.bitwise_and(img, img_inv)
        img = cv2.bitwise_or(img, img_canvas)
    else:
        print(f"Image size mismatch: img={img.shape}, img_inv={img_inv.shape}, img_canvas={img_canvas.shape}")

     
    cv2.rectangle(img, (250, 10), (450, 100), (0, 0, 255), cv2.FILLED) # Red
    cv2.rectangle(img, (550, 10), (750, 100), (0, 255, 0), cv2.FILLED) # Green
    cv2.putText(img, "ERASER", (850, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Air Canvas", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break