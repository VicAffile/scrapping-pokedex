from selenium import webdriver

from classes.pokemon import Pokemon

pokepedia = webdriver.Chrome(executable_path="chromedriver.exe")
pokepedia.get("https://www.pokepedia.fr/Tortipouss")

pokemon = Pokemon(pokepedia)
pokemon.afficher()

pokepedia.quit()