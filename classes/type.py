from selenium.webdriver.common.by import By


class Type:

    def __init__(self, pokepedia):
        self.nom = ""

        self.scrapping(pokepedia)

    def scrapping(self, pokepedia):
        self.obtenir_nom(pokepedia)

    def afficher(self):
        print("Type : " + self.nom)

    def obtenir_nom(self, pokepedia):
        self.nom = pokepedia.find_element(By.XPATH, "//h1[@id='firstHeading']").text
