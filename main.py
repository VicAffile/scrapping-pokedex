import pymongo
from dotenv import load_dotenv
import os
import unidecode as unidecode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from classes.pokemon import Pokemon
from classes.type import Type


scrapper_pokemons = True
scrapper_types = False

chrome_options = Options()
chrome_options.add_argument("--headless")

load_dotenv()
BDD_UTILISATEUR = os.getenv("BDD_UTILISATEUR")
BDD_MOTDEPASSE = os.getenv("BDD_MOTDEPASSE")

client = pymongo.MongoClient("mongodb+srv://" + BDD_UTILISATEUR + ":" + BDD_MOTDEPASSE + "@pokemon.svi0i.mongodb.net/pokemon")
bdd_nom = client["pokedex"]


if scrapper_pokemons:
    collection_nom = bdd_nom["pokemons"]

    pokemon_annuaire = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
    pokemon_annuaire.get("https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_dans_l%27ordre_du_Pok%C3%A9dex_National")

    liste_pokemons = []
    pokemons = pokemon_annuaire.find_elements(By.XPATH, "//table[@class='tableaustandard sortable entetefixe jquery-tablesorter' or @class='tableaustandard centre sortable entetefixe jquery-tablesorter']//tbody//tr//td[3]")
    for pokemon in pokemons:
        region = str(pokemon.text).split(" ")[0]
        if region != "Alolan" and region != "Galarian" and region != "Hisuian":
            liste_pokemons.append(pokemon.text)

    for filename in os.listdir("images/mignatures"):
        os.remove("images/mignatures/" + filename)
    for filename in os.listdir("images/sprites"):
        os.remove("images/sprites/" + filename)

    index = 16
    max = 26
    liste_pokemon_scrap = []
    while index - 1 < max:
        liste_pokemon_scrap.append(liste_pokemons[index - 1])
        index += 1


    pokemon_pokepedia = None
    pokemon_pokebip = None

    for pokemon in liste_pokemon_scrap:

        nom_pokepedia = pokemon
        if pokemon == "Nidoran♀":
            nom_pokebip = "nidoran-f"
        elif pokemon == "Nidoran♂":
            nom_pokebip = "nidoran-m"
        else:
            nom_pokebip = unidecode.unidecode(pokemon.lower())

        pokemon_pokepedia = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
        pokemon_pokepedia.get("https://www.pokepedia.fr/" + nom_pokepedia)
        pokemon_pokebip = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
        pokemon_pokebip.get("https://www.pokebip.com/pokedex/pokemon/" + nom_pokebip)

        scrapp = Pokemon(pokemon_pokepedia, pokemon_pokebip, pokemon_annuaire)
        scrapp.afficher()
        pokemon = {
            "numero": scrapp.numero,
            "nom_fr": scrapp.nom_fr,
            "nom_jap": scrapp.nom_jap,
            "mignature": scrapp.mignature,
            "sprite": scrapp.sprite,
            "type": scrapp.type,
            "categorie": scrapp.categorie,
            "taille": scrapp.taille,
            "poids": scrapp.poids,
            "talent": scrapp.talent,
            "groupe_oeuf": scrapp.groupe_oeuf,
            "pas_eclosion": scrapp.pas_eclosion,
            "nom_preevolution": scrapp.nom_preevolution,
            "nom_evolution": scrapp.nom_evolution,
            "condition_evolution": scrapp.condition_evolution,
            "description": scrapp.description
        }
        if collection_nom.find_one({'numero': scrapp.numero}) is not None:
            collection_nom.delete_many({'numero': scrapp.numero})
        collection_nom.insert_one(pokemon)
        print(" ")

    pokemon_pokepedia.close()
    pokemon_pokebip.close()
    pokemon_annuaire.close()


if scrapper_types:
    collection_nom = bdd_nom["types"]

    type_annuaire = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
    type_annuaire.get("https://www.pokepedia.fr/Type")

    liste_types = []
    types = type_annuaire.find_elements(By.XPATH, "//table[@class='tableaustandard navigation']//td[@colspan='2']//a")
    for type in types:
        nom = type.get_attribute("title").split(" ")[0]
        liste_types.append(nom) if nom != "Combat" and nom != "Vol" and nom != "Poison" and nom != "Ténèbres" and nom != "Fée" else liste_types.append(nom + "_(type)")

    for filename in os.listdir("images/types"):
        os.remove("images/types/" + filename)

    for type in liste_types:

        type_pokepedia = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=chrome_options)
        type_pokepedia.get("https://www.pokepedia.fr/" + type)

        scrapp = Type(type_pokepedia)
        scrapp.afficher()
        type = {
            "nom": scrapp.nom,
            "image": scrapp.image
        }
        collection_nom.insert_one(type)
        print(" ")

        type_pokepedia.close()

    type_annuaire.close()

print("SCRAP FINI!!!")
