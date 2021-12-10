import pymongo
from dotenv import load_dotenv
import os
import unidecode as unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from numpy import asarray
from PIL import Image
import blosc

from classes.pokemon import Pokemon


load_dotenv()
BDD_UTILISATEUR = os.getenv('BDD_UTILISATEUR')
BDD_MOTDEPASSE = os.getenv('BDD_MOTDEPASSE')

client = pymongo.MongoClient("mongodb+srv://" + BDD_UTILISATEUR + ":" + BDD_MOTDEPASSE + "@pokemon.svi0i.mongodb.net/pokemon")
bdd_nom = client['pokedex']
collection_nom = bdd_nom['pokemons']

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

index = 385
max = 397
liste_pokemon_scrap = []
while index < max:
    index += 1
    liste_pokemon_scrap.append(liste_pokemon[index])


pokepedia = None
pokebip = None

for pokemon in liste_pokemon_scrap:

    nom_pokepedia = pokemon
    if pokemon == "Nidoran♀":
        nom_pokebip = "nidoran-f"
    elif pokemon == "Nidoran♂":
        nom_pokebip = "nidoran-m"
    else:
        nom_pokebip = unidecode.unidecode(pokemon.lower())

    pokepedia = webdriver.Chrome(executable_path="chromedriver.exe")
    pokepedia.get("https://www.pokepedia.fr/" + nom_pokepedia)
    pokebip = webdriver.Chrome(executable_path="chromedriver.exe")
    pokebip.get("https://www.pokebip.com/pokedex/pokemon/" + nom_pokebip)

    scrapp = Pokemon(pokepedia, pokebip, annuaire)
    scrapp.afficher()
    pokemon = {
        "numero": scrapp.numero,
        "nom_fr": scrapp.nom_fr,
        "nom_jap": scrapp.nom_jap,
        "mignature": blosc.pack_array(asarray(Image.open(scrapp.mignature))),
        "sprite": blosc.pack_array(asarray(Image.open(scrapp.sprite))),
        "type": scrapp.type,
        "categorie": scrapp.categorie,
        "talent": scrapp.talent,
        "groupe_oeuf": scrapp.groupe_oeuf,
        "pas_eclosion": scrapp.pas_eclosion,
        "nom_preevolution": scrapp.nom_preevolution,
        "nom_evolution": scrapp.nom_evolution,
        "condition_evolution": scrapp.condition_evolution,
        "description": scrapp.description
    }
    collection_nom.insert_one(pokemon)
    print(" ")

pokepedia.close()
pokebip.close()
annuaire.close()
