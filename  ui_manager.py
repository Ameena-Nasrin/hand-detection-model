import cv2
import numpy as np

class UIManager:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        
     
        self.colors = {
            "Blue": (255, 0, 0),
            "Green": (0, 255, 0),
            "Red": (0, 0, 255),
            "Yellow": (0, 255, 255),
            "Eraser": (0, 0, 0)
        }
        
         
        self.current_color = self.colors["Blue"]
        self.brush_thickness = 5
        self.eraser_thickness = 50

    def draw_header(self, frame):
        """
        Draws the top selection bar with color boxes.
        """
         cv2.rectangle(frame, (0, 0), (self.width, 100), (45, 45, 45), -1)
        cv2.line(frame, (0, 100), (self.width, 100), (255, 255, 255), 2)

        
        cv2.rectangle(frame, (20, 10), (220, 90), self.colors["Blue"], -1)
        cv2.putText(frame, "BLUE", (85, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (250, 10), (450, 90), self.colors["Green"], -1)
        cv2.putText(frame, "GREEN", (310, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (480, 10), (680, 90), self.colors["Red"], -1)
        cv2.putText(frame, "RED", (555, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.rectangle(frame, (710, 10), (910, 90), self.colors["Yellow"], -1)
        cv2.putText(frame, "YELLOW", (775, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        cv2.rectangle(frame, (940, 10), (1260, 90), (255, 255, 255), -1)
        cv2.putText(frame, "ERASER / CLEAR", (1000, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        return frame

    def get_selection(self, x, y):
        """
        Logic for Phase 3: Detects if the index tip is within a UI Zone.
        Returns the color and brush thickness.
        """
        if y < 100:
            if 20 < x < 220:
                self.current_color = self.colors["Blue"]
            elif 250 < x < 450:
                self.current_color = self.colors["Green"]
            elif 480 < x < 680:
                self.current_color = self.colors["Red"]
            elif 710 < x < 910:
                self.current_color = self.colors["Yellow"]
            elif 940 < x < 1260:
                self.current_color = self.colors["Eraser"]
        
        return self.current_color

    def draw_cursor(self, frame, x, y, mode):
        """
        Visual feedback for the user based on the Phase 3 Decision Tree.
        """
        color = (255, 255, 255) # Default White
        label = "Hover"
        
        if mode == "Drawing":
            color = self.current_color
            label = "Drawing..."
        elif mode == "Selection":
            color = (0, 255, 255)
            label = "Selecting"

         
        cv2.circle(frame, (x, y), 10, color, cv2.FILLED)
        cv2.putText(frame, label, (x + 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return frame