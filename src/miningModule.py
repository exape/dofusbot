import mss
import numpy as np
import cv2
import pyautogui
from ultralytics import YOLO
import datetime
import time

class Mining:

    def setupMining(self):
        print("Mining selectionné")
        self.mine()

    def pointCursorToOre(self, coordinates):
        x, y = coordinates[0], coordinates[1]
        pyautogui.moveTo(x, y)

    def clickOre(self, coordinates):
        x, y = coordinates[0], coordinates[1]
        pyautogui.click(x, y)

    def doScreenshot(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
        return img
            
    def findOre(self, image):
        coordinates_list = []
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        model = YOLO("best.pt")
        image = image[:,:,:3]
        results = model.predict(image, conf=.7)
        for box in results[0].boxes:
            box_coordinates = (box.xyxy).tolist()[0]
            left, top, right, bottom = int(box_coordinates[0]), int(box_coordinates[1]), int(box_coordinates[2]), int(box_coordinates[3])
            box_coordinates = (left, top, right, bottom)
            x = ((left + right) / 2)
            y = ((top + bottom) / 2)
            coordinate = ((x,y), box_coordinates)
            coordinates_list.append(coordinate)
        if(len(coordinates_list) != 0):
            print("findOre: " + str(len(coordinates_list)) + " minerais trouvé(s) à " + current_time)
            return coordinates_list
        else:
            return None

    def filterOre(self, coordinates, image):
        mask = np.zeros(image.shape[:2], dtype="uint8")
        left, top, right, bottom = coordinates[1][0], coordinates[1][1], coordinates[1][2], coordinates[1][3]
        cv2.rectangle(mask, (left - 200, top - 200), (right + 200, bottom + 200), (255, 255, 255), -1)
        image = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("test", image)
        cv2. waitKey(0)
        # TODO: read text from image cropped
        # If the player has the level to mine the ore, return true
        return True
        
    def mine(self):
        try:
            while True:
                image = self.doScreenshot()
                coordinates_list = self.findOre(image)
                if coordinates_list is not None:
                    for coordinates in coordinates_list:
                        self.pointCursorToOre(coordinates[0])
                        time.sleep(.5)
                        image_with_ore_selected = self.doScreenshot()
                        adequate_level = self.filterOre(coordinates, image_with_ore_selected)
                else:
                    print("mine: " + "Aucun minerai trouvé sur l'écran")
        except KeyboardInterrupt:
            print("Interruption du programme par ctrl+c")