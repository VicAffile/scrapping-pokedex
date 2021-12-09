from selenium.webdriver.common.by import By


class Pokemon:

    def __init__(self, pokepedia):
        self.numero = 0
        self.nom_fr = ""
        self.nom_jap = ""

        self.scrapping(pokepedia)


    def scrapping(self, pokepedia):
        self.obtenir_numero(pokepedia)
        self.obtenir_nom_fr(pokepedia)
        self.obtenir_nom_jap(pokepedia)

    def afficher(self):
        print("Numéro : n°" + str(self.numero))
        print("Nom fr : " + self.nom_fr)
        print("Nom jap : " + self.nom_jap)

    def obtenir_numero(self, pokepedia):
        self.numero = pokepedia.find_element(By.XPATH, "//div[@id='mw-content-text']//table[1]//tr[2]//td[2]").text

    def obtenir_nom_fr(self, pokepedia):
        self.nom_fr = pokepedia.find_element(By.ID, "firstHeading").text

    def obtenir_nom_jap(self, pokepedia):
        self.nom_jap = pokepedia.find_element(By.XPATH, "//span[@title='Nom déposé officiel']//i").text
