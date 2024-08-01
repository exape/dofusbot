import mss
import numpy as np
import cv2
import pyautogui
from ultralytics import YOLO
from src.ore import Ore

class Mining:

    model = YOLO("best.pt")

    def setupMining(self):
        print("Mining selectionné")
        self.mine()

    def mine(self):
        try:
            while True:
                image = self.doScreenshot()
                ores = self.findOre(image)
                if ores is not None:
                    for ore in ores:
                        self.pointCursorToOre(ore=ore)
                        image_with_ore_selected = self.doScreenshot()
                        adequate_level = self.filterOre(ore, image_with_ore_selected)
                else:
                    print("mine: " + "Aucun minerai trouvé sur l'écran")
        except KeyboardInterrupt:
            print("Interruption du programme par ctrl+c")

    def pointCursorToOre(self, ore: Ore):
        pyautogui.moveTo(ore.x, ore.y)

    def clickOre(self, ore: Ore):
        pyautogui.click(ore.x, ore.y)

    def doScreenshot(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
        return img
            
    def findOre(self, image):
        ores = []
        image = image[:,:,:3]
        results = self.model.predict(image, conf=.7)
        for box in results[0].boxes:
            box_coordinates = (box.xyxy).tolist()[0]
            ore = Ore(x=(int(box_coordinates[0]) + int(box_coordinates[2])) / 2, y=(int(box_coordinates[1]) + int(box_coordinates[3])) / 2, left=int(box_coordinates[0]) , top=int(box_coordinates[1]) , right=int(box_coordinates[2]) , bottom=int(box_coordinates[3]))
            ores.append(ore)
        if(len(ores) != 0):
            return ores
        else:
            return None

    def filterOre(self, ore: Ore, image):
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (ore.left - 200, ore.top - 200), (ore.right + 200, ore.bottom + 200), (255, 255, 255), -1)
        image = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow("test", image)
        cv2. waitKey(0)
        # TODO: read text from image cropped
        # If the player has the level to mine the ore, return true
        return True
        
