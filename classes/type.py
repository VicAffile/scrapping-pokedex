import os

import wget
from selenium.webdriver.common.by import By


class Type:

    def __init__(self, pokepedia):
        self.nom = ""
        self.image = ""

        self.scrapping(pokepedia)

    def scrapping(self, pokepedia):
        self.obtenir_nom(pokepedia)
        self.obtenir_image(pokepedia)

    def afficher(self):
        print("Type : " + self.nom)
        print("Image : " + self.image)

    def obtenir_nom(self, pokepedia):
        self.nom = pokepedia.find_element(By.XPATH, "//h1[@id='firstHeading']").text.split(" ")[0]

    def obtenir_image(self, pokepedia):
        self.image = "type_" + self.nom + ".png"
