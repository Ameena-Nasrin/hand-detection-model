import numpy as np
import time

class CanvasUtils:
    def __init__(self, smoothing_factor=0.7):
        """
        :param smoothing_factor: Value between 0 and 1. 
                                Higher = smoother but more lag.
                                Lower = more responsive but more jitter.
        """
        self.smoothing = smoothing_factor
        self.prev_x, self.prev_y = 0, 0

    def smooth_coordinates(self, curr_x, curr_y):
        """Applies EMA to coordinates to prevent shaky lines."""
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = curr_x, curr_y
            return curr_x, curr_y

        smooth_x = int(self.smoothing * self.prev_x + (1 - self.smoothing) * curr_x)
        smooth_y = int(self.smoothing * self.prev_y + (1 - self.smoothing) * curr_y)
        
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y

    def reset_smoothing(self):
        """Call this whenever the hand is lost or a stroke ends."""
        self.prev_x, self.prev_y = 0, 0

def calculate_fps(prev_time):
    """Calculates and returns the Frames Per Second."""
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    return fps, curr_time

def get_distance(p1, p2):
    """Calculates Euclidean distance between two landmarks (e.g., for pinch)."""
    return np.hypot(p2[0] - p1[0], p2[1] - p1[1])