import mss
import numpy as np

class Mining:
    method = ""
    treshold = 0

    def __init__(self, m, t):
        self.method = m
        self.treshold = t

    def doScreenshot(m):
        with mss.mss() as sct:
            monitor = sct.monitors[m]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
        return img
    
    def findTemplate(i, t, tr):
        return None