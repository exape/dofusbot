import mss
import numpy as np
import cv2
import pyautogui
from ultralytics import YOLO
import datetime
import time

class Mining:

    def doScreenshot(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
        return img
    
    def setupMining(self):
        print("Mining selectionné")
        self.mine()
            
    def findOre(self):
        print("=========================================")
        coordinates = []
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        model = YOLO("best.pt")
        image = self.doScreenshot()
        image2 = image
        image = image[:,:,:3]
        results = model.predict(image, conf=.7)
        for box in results[0].boxes:
            box_coordinates = (box.xyxy).tolist()[0]
            left, top, right, bottom = box_coordinates[0], box_coordinates[1], box_coordinates[2], box_coordinates[3]
            cv2.rectangle(image2, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0), 2)
            x = int((left + right) / 2)
            y = int((top + bottom) / 2)
            cv2.circle(image2, (x, y), 2, (255, 0, 0), 2)
            coordinate = (x,y)
            coordinates.append(coordinate)
            print("findOre: " + "Minerais trouvé(s) à " + current_time)
            return coordinates
        return None

    def filterOre(self, coordinates):
        print("=========================================")
        print("filterOre: " + " Filtrage des minerais présents sur la map")
        print(coordinates[0])

    def mine(self):
        coordinates = self.findOre()
        if coordinates is not None:
            self.filterOre(coordinates)