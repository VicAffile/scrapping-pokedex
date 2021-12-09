import os
import unidecode as unidecode
from selenium import webdriver

from classes.pokemon import Pokemon


for filename in os.listdir("images/sprites"):
    os.remove("images/sprites/" + filename)

nom_pokepedia = "Amphinobi"
nom_pokebip = unidecode.unidecode(nom_pokepedia.lower())

pokepedia = webdriver.Chrome(executable_path="chromedriver.exe")
pokepedia.get("https://www.pokepedia.fr/" + nom_pokepedia)
pokebip = webdriver.Chrome(executable_path="chromedriver.exe")
pokebip.get("https://www.pokebip.com/pokedex/pokemon/" + nom_pokebip)

pokemon = Pokemon(pokepedia, pokebip)
pokemon.afficher()

pokepedia.close()
pokebip.close()
