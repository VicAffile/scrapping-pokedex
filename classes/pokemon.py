from selenium.webdriver.common.by import By


class Pokemon:

    def __init__(self, pokepedia, pokebip):
        self.numero = 0
        self.nom_fr = ""
        self.nom_jap = ""
        self.type = []
        self.categorie = ""
        self.talent = []
        self.groupe_oeuf = []
        self.pas_eclosion = ""
        self.nom_preevolution = ""
        self.nom_evolution = []
        self.condition_evolution = []

        self.scrapping(pokepedia, pokebip)


    def scrapping(self, pokepedia, pokebip):
        self.obtenir_numero(pokepedia)
        self.obtenir_nom_fr(pokepedia)
        self.obtenir_nom_jap(pokepedia)
        self.obtenir_categorie(pokepedia)
        self.obtenir_type(pokepedia)
        self.obtenir_talent(pokepedia)
        self.obtenir_infos_oeuf(pokepedia)
        self.obtenir_evolution(pokebip)

    def afficher(self):
        print("Numéro : n°" + str(self.numero))
        print("Nom fr : " + self.nom_fr)
        print("Nom jap : " + self.nom_jap)
        print("Type : " + str(self.type))
        print("Catégorie : " + self.categorie)
        print("Talent : " + str(self.talent))
        print("Groupe-oeuf : " + str(self.groupe_oeuf))
        print("Temps éclosion : " + self.pas_eclosion)
        print("Pré-évolution : " + self.nom_preevolution)
        print("Evolution(s) : " + str(self.nom_evolution))
        print("Condition(s) d'évolutions : " + str(self.condition_evolution))

    def obtenir_numero(self, pokepedia):
        self.numero = pokepedia.find_element(By.XPATH, "//div[@id='mw-content-text']//table[1]//tr[2]//td[2]").text

    def obtenir_nom_fr(self, pokepedia):
        self.nom_fr = pokepedia.find_element(By.ID, "firstHeading").text

    def obtenir_nom_jap(self, pokepedia):
        self.nom_jap = pokepedia.find_element(By.XPATH, "//span[@title='Nom déposé officiel']//i").text

    def obtenir_type(self, pokepedia):
        types = pokepedia.find_elements(By.XPATH, "//div[@id='mw-content-text']//div[@class='mw-parser-output']//table[2]//tr[7]//td//a")
        for type in types:
            self.type.append(type.get_attribute("title").split(" ")[0])

    def obtenir_categorie(self, pokepedia):
        self.categorie = pokepedia.find_element(By.XPATH, "//div[@id='mw-content-text']//div[@class='mw-parser-output']//table[2]//tr[8]//td").text

    def obtenir_talent(self, pokepedia):
        talents = pokepedia.find_elements(By.XPATH, "//div[@id='mw-content-text']//div[@class='mw-parser-output']//table[2]//tr[11]//td//a")
        for talent in talents:
            if talent.text != "Talent caché":
                self.talent.append(talent.text)

    def obtenir_infos_oeuf(self, pokepedia):
        groupes_oeuf = pokepedia.find_elements(By.XPATH, "//div[@id='mw-content-text']//div[@class='mw-parser-output']//table[2]//tr[12]//td//a")
        for groupe_oeuf in groupes_oeuf:
            self.groupe_oeuf.append(groupe_oeuf.text)
        self.pas_eclosion = str(pokepedia.find_element(By.XPATH, "//div[@id='mw-content-text']//div[@class='mw-parser-output']//table[2]//tr[13]//td").text)

    def obtenir_evolution(self, pokebip):
        nombre_colonne = len(pokebip.find_elements(By.XPATH,
                                                   "//div[@id='section-evolutions']//div[1]//div[@class='col-sm-3 col-xs-12']"))
        nom_derniere_colonne = list(pokebip.execute_script(
            "return document.getElementById('section-evolutions').getElementsByClassName('col-sm-3 col-xs-12')[" + str(
                nombre_colonne - 1) + "].getElementsByClassName('panel-heading')[0].textContent"))
        retour = []
        for lettre in nom_derniere_colonne:
            if lettre != " " and lettre != "\n":
                retour.append(lettre)
        nombre_colonne -= 1 if str("".join(retour)) == "Stadespécial" else 0
        if nombre_colonne == 1:
            self.nom_preevolution = "Aucune"
            self.nom_evolution = ["Aucune"]
            self.condition_evolution = ["Aucune"]
            return
        else:
            stade_initial = pokebip.execute_script(
                "return document.getElementById('section-evolutions').getElementsByClassName('col-sm-3 col-xs-12')[0].querySelector('ul').querySelectorAll('div')[1].querySelector('a').textContent")
            nombre_pokemon_stade_1 = len(pokebip.find_elements(By.XPATH,
                                                               "//div[@id='section-evolutions']//div[1]//div[@class='col-sm-3 col-xs-12'][2]//ul//li")) if nombre_colonne >= 2 else None
            nombre_pokemon_stade_2 = len(pokebip.find_elements(By.XPATH,
                                                               "//div[@id='section-evolutions']//div[1]//div[@class='col-sm-3 col-xs-12'][3]//ul//li")) if nombre_colonne == 3 else None
            pokemon_stade_1 = self.obtenir_pokemon_stade(pokebip, nombre_pokemon_stade_1,
                                                         1) if nombre_pokemon_stade_1 != None else ["Aucune"]
            condition_stade_1 = self.obtenir_condition_stade(pokebip, nombre_pokemon_stade_1,
                                                             1) if nombre_pokemon_stade_1 != None else ["Aucune"]
            pokemon_stade_2 = self.obtenir_pokemon_stade(pokebip, nombre_pokemon_stade_2,
                                                         2) if nombre_pokemon_stade_2 != None else ["Aucune"]
            condition_stade_2 = self.obtenir_condition_stade(pokebip, nombre_pokemon_stade_2,
                                                             2) if nombre_pokemon_stade_2 != None else ["Aucune"]
            if self.nom_fr == stade_initial:
                self.nom_preevolution = "Aucune"
                self.nom_evolution = pokemon_stade_1
                self.condition_evolution = condition_stade_1
                return
            elif nombre_colonne == 2:
                self.nom_preevolution = stade_initial
                self.nom_evolution = ["Aucune"]
                self.condition_evolution = ["Aucune"]
                return
            elif nombre_colonne == 3:
                for pokemon in pokemon_stade_1:
                    if self.nom_fr == pokemon:
                        self.nom_preevolution = stade_initial
                        self.nom_evolution = pokemon_stade_2
                        self.condition_evolution = condition_stade_2
                        return
                for pokemon in pokemon_stade_2:
                    if self.nom_fr == pokemon:
                        self.nom_preevolution = pokemon_stade_1[0]
                        self.nom_evolution = ["Aucune"]
                        self.condition_evolution = ["Aucune"]
                        return

    def obtenir_pokemon_stade(self, pokebip, nombre_pokemon, stade):
        pokemon_stade = []
        pokemon = 0
        continuer = True
        while continuer:
            pokemon_stade.append(pokebip.execute_script(
                "return document.getElementById('section-evolutions').getElementsByClassName('col-sm-3 col-xs-12')[" + str(
                    stade) + "].querySelector('ul').querySelectorAll('li')[" + str(
                    pokemon) + "].querySelectorAll('div')[1].querySelector('a').textContent"))
            pokemon += 1
            if pokemon == nombre_pokemon:
                continuer = False
        return pokemon_stade

    def obtenir_condition_stade(self, pokebip, nombre_pokemon, stade):
        condition_stade = []
        pokemon = 0
        continuer = True
        while continuer:
            condition = self.format_condition_evolution(pokebip.execute_script(
                "return document.getElementById('section-evolutions').getElementsByClassName('col-sm-3 col-xs-12')[" + str(
                    stade) + "].querySelector('ul').querySelectorAll('li')[" + str(
                    pokemon) + "].querySelectorAll('div')[1].textContent"))
            condition_stade.append(condition)
            pokemon += 1
            if pokemon == nombre_pokemon:
                continuer = False
        return condition_stade

    def format_condition_evolution(self, condition):
        condition = list(condition.split("\n")[3])
        espace = True
        while espace:
            if condition[0] == " ":
                condition = condition[1:]
            else:
                espace = False
        return str("".join(condition))
