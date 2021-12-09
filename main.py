import os
import unidecode as unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By

from classes.pokemon import Pokemon


annuaire = webdriver.Chrome(executable_path="chromedriver.exe")
annuaire.get("https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_dans_l%27ordre_du_Pok%C3%A9dex_National")

liste_pokemon = []
pokemons = annuaire.find_elements(By.XPATH, "//table[@class='tableaustandard sortable entetefixe jquery-tablesorter' or @class='tableaustandard centre sortable entetefixe jquery-tablesorter']//tbody//tr//td[3]")
for pokemon in pokemons:
    region = str(pokemon.text).split(" ")[0]
    if region != "Alolan" and region != "Galarian" and region != "Hisuian":
        liste_pokemon.append(pokemon.text)

for filename in os.listdir("images/mignatures"):
    os.remove("images/mignatures/" + filename)
for filename in os.listdir("images/sprites"):
    os.remove("images/sprites/" + filename)

nom_pokepedia = "Amphinobi"
nom_pokebip = unidecode.unidecode(nom_pokepedia.lower())

pokepedia = webdriver.Chrome(executable_path="chromedriver.exe")
pokepedia.get("https://www.pokepedia.fr/" + nom_pokepedia)
pokebip = webdriver.Chrome(executable_path="chromedriver.exe")
pokebip.get("https://www.pokebip.com/pokedex/pokemon/" + nom_pokebip)

pokemon = Pokemon(pokepedia, pokebip, annuaire)
pokemon.afficher()

pokepedia.close()
pokebip.close()
annuaire.close()
