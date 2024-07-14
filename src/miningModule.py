import mss
import numpy as np
import cv2
import pyautogui
from ultralytics import YOLO

class Mining:

    def doScreenshot(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
        return img
    
    def setupMining(self):
        print("Mining selectionné")
        self.find()

    def find(self):
        print("DEBUG: Using yolov8 nano")
        
        model = YOLO("src/last.pt")

        image = self.doScreenshot()
        image = image[:,:,:3]

        results = model.predict(image)


        for box in results[0].boxes:
            print(box.xyxy)

        cv2.imshow("test", image)
        cv2.waitKey(0)

    def clickOre(self, coordinates):
        print("DEBUG: Clic aux coordonées:")
        pyautogui.click(button="left", x=coordinates[0], y=coordinates[1])