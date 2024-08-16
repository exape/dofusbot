import mss
import numpy as np
import cv2
import pyautogui
from ultralytics import YOLO
from src.ore import Ore
import pytesseract
import time
import asyncio

class Mining:

    model = YOLO("best.pt")

    def setupMining(self) -> None:
        print("Mining selectionné")
        self.mine()

    def mine(self) -> None:
        try:
            while True:
                # Checking every ore from the screenshot taken
                image = self.doScreenshot()
                ores = self.findOre(image)
                if ores is not None:
                    for ore in ores:
                        self.pointCursorToOre(ore=ore)
                        image_with_ore_selected = self.doScreenshot()
                        # Awaiting for text reading
                        loop = asyncio.get_event_loop()
                        task = loop.create_task(self.filterOre(ore, image_with_ore_selected))
                        result = loop.run_until_complete(task)
                        if "fer" in result.lower():
                            print("mine: " + "Fer trouvé")
                            self.clickOre(ore)
                        else:
                            print("mine: " + "minerai non reconnu")
                else:
                    print("mine: " + "Aucun minerai trouvé sur l'écran")
        except KeyboardInterrupt:
            print("Programme terminé par Ctrl + C")

    def pointCursorToOre(self, ore: Ore) -> None:
        pyautogui.moveTo(ore.x, ore.y)
        # Fixing blurry screenshots taken when the game takes some frames to display the ore nameplate
        time.sleep(1)

    def clickOre(self, ore: Ore) -> None:
        pyautogui.click(ore.x, ore.y)

    def doScreenshot(self) -> np.array:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
        return img
            
    def findOre(self, image) -> list | None:
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

    async def filterOre(self, ore: Ore, image) -> str:
        print("filtering...")
        # Crop image to a smaller region (TODO: crop based on screen %)
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (ore.left, ore.top - 100), (ore.right + 200, ore.bottom), (255, 255, 255), -1)
        image = cv2.bitwise_and(image, image, mask=mask)
        # Convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        _, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
        # Read text from cropped image
        text = pytesseract.image_to_string(image, config='--oem 3 --psm 6')
        return text