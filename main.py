from selenium import webdriver

from classes.pokemon import Pokemon

pokepedia = webdriver.Chrome(executable_path="chromedriver.exe")
pokepedia.get("https://www.pokepedia.fr/Chenipotte")
pokebip = webdriver.Chrome(executable_path="chromedriver.exe")
pokebip.get("https://www.pokebip.com/pokedex/pokemon/chenipotte")

pokemon = Pokemon(pokepedia, pokebip)
pokemon.afficher()

pokepedia.close()
pokebip.close()
