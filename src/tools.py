import mss
import numpy as np
import cv2
import pyautogui
from ultralytics import YOLO
from src.ore import Ore
import pytesseract
import time
import asyncio
import json
import re
import unidecode

class Mining:

    # Model for ore detection
    model = YOLO("best.pt")
    # JSON loads
    config = json.load(open("config.json"))
    ore_list = config["orelist"]
    regex_list = config["regexlist"]
    # Text filter when reading an image
    filter_alphanumeric = re.compile('[^a-zA-Z]')

    def setupMining(self) -> None:
        print("Mining selectionné, liste des minerais à chercher:")
        for ore in self.ore_list:
            print(ore)
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
                        # Preparing text to remove false positives from text reading
                        result = result.replace("\n", "")
                        result = result.replace(" ", "")
                        result = unidecode.unidecode(result)
                        result = self.filter_alphanumeric.sub('', result).lower()
                        # Finding an occudrence on the given string
                        for regex in self.regex_list:
                            # Find the ore name in the messy string
                            match = re.search(regex, result)
                            if match is not None:
                                print("J'ai trouvé un minerai qui est dans la config:")
                                print(match.group())
                                self.clickOre(ore=ore)
                                time.sleep(5)
                                break
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