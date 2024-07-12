import mss
import numpy as np
import cv2 as cv
import math
import pyautogui

class Mining:
    method = int
    threshold = None
    templates = [
        "ressource/miningTemplates/ore_alt.png"
    ]

    def getMethod(self):
        return self.method
    
    def setMethod(self, value):
        self.method = value

    def getThreshold(self):
        return self.threshold
    
    def setThreshold(self, value):
        self.treshold = value

    def doScreenshot(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
        return img
    
    def setupMining(self):
        print("Mining selectionné")
        print("Saisir la méthode de detection par OpenCV:")
        print("1 pour TM_CCOEFF_NORMED")
        print("2 pour TM_CCORR_NORMED")
        print("3 pour sortir du programme")
        choice_method = input("Choix: ")
        match choice_method:
            case "3":
                exit(0)
            case "1":
                self.setMethod(cv.TM_CCOEFF_NORMED)
            case "2":
                self.setMethod(cv.TM_CCORR_NORMED)
            case _:
                print("Erreur de saisie. Veuillez vérifier la syntaxe et ré-essayer.")
                exit(1)
        print("Saisir la sensibilité de détection d'OpenCV:")
        print("Exemple de valeur à saisir entre 0 et 1. ex: 0.5")
        try:
            choice_threshold = float(input("Choix: "))
        except ValueError:
            print("Erreur de saisie. Veuillez vérifier la syntaxe et ré-essayer.")
            exit(1)
        if choice_threshold > 0 and choice_threshold < 1:
            self.threshold = choice_threshold
            self.find()
        else:
            print("La valeur est incorrecte. Veuillez vérifier et ré-essayer.")
            exit(1)
        

    def find(self):
        for x in self.templates:
            print("DEBUG: " + "Using template " + x)
            screenshot = self.doScreenshot()
            img_gray = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
            template = cv.imread(x, cv.IMREAD_GRAYSCALE)
            results = cv.matchTemplate(img_gray,template, self.getMethod())
            filtered_results = np.where(results >= self.getThreshold())
            if len(filtered_results[0]) > 1:
                print("DEBUG: " + "OpenCV a detecté un minerai à l'écran")
                coords = []
                for pt in zip(*filtered_results[::-1]):
                    coords += [(pt[0], pt[1])]
                coords.sort(key=lambda x: math.sqrt((x[0] - 960) ** 2 + (x[1] - 540) ** 2))
                self.clickOre(coords[0])
                print(coords)
            else:
                print("DEBUG: Aucun minerai detecté")

    def clickOre(self, coordinates):
        print("DEBUG: Clic aux coordonées:")
        pyautogui.click(button="right", x=coordinates[0], y=coordinates[1])