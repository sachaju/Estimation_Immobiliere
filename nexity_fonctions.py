import random
import re
import seaborn as sns
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import orpi_fonctions as orpi
import nexity_fonctions as nexity
import lefigaro_fonctions as lefigaro
import basics_estimations_fonctions as basics

# a) Localisation : Ville et Quartier
def localisation(soup):
    """
    Récupération de la ville et du quartier pour un logement d'une annonce du site "nexity".
    """
    ville = soup.find("span", class_='city').text
    if ville == "Strasbourg":
        quartiers = ["meinau", "neustadt", 'poteries', "esplanade", "petite france", "cronenbourg", "koenigshoffen", "halles", "neudorf", "robertsau", "gare", "musau", "orangerie", "krutenau", "forêt noire", 'centre-ville', "port du rhin", "hautepierre", "contades", "tribunal", "neuhof", "montagne verte"]
        text = soup.find("div", class_='description text_body_1 mt-2').text.lower().split()
        quartier = "nan"
        for i in range(len(quartiers)):
            for j in range(len(text)):
                if quartiers[i] in text[j]:
                    quartier = quartiers[i].capitalize()
                    break
    else:
        quartier = ville
    return [ville, quartier]

# b) Prix et honoraires :
def price(soup):
    """
    Récupération du prix et du montant des honoraires pour un logement d'une annonce "nexity".
    """
    prix = float(soup.find_all("h2", class_="text text--small text--hightlighted text--hightlighted--not-new")[0].text.replace(" €", "").replace(" ", ""))
    text = soup.find("div", class_="text text--small--honoraires").text
    if "vendeur" in text:
        honoraires = float(0)
    else:
        honoraires = float("nan")
    return [prix, honoraires] 

# c) caractéristiques : "pièce(s)", "surface", "ascenseur", "balcon", "terrasse", "cave", "parking" et "terrain"
def options(soup):  
    """
    Récupération des options disponibles pour un logement d'une annonce "nexity".
    Options : "Pièces", "surface", "Ascenseur", "Balcon", "Terrasse", "Cave", "Garage", "Terrain".
    """
    variables = ["pièce(s)", "surface", "ascenseur", "balcon", "terrasse", "cave", "parking", "terrain"]
    caracteristiques = list(np.zeros(len(variables), dtype=float))
    text = soup.find_all("div", class_='d-flex align-items-center')
    for i in range(len(text)):
        element = text[i].text.lower()
        for j in range(len(variables)):
            if variables[j] in element:
                caracteristiques[j] = element.split()[len(element.split())-1].capitalize()
                break
    caracteristiques[1] = caracteristiques[1].replace('m²', '')
    for i in [0,1]:
        caracteristiques[i] = float(caracteristiques[i])
    for j in [2,3,4,5,6,7]:
        if caracteristiques[j] == "Non":
            caracteristiques[j] = float(0)
        else:
            caracteristiques[j] = float(1)
    return caracteristiques

# Fonction qui nous donne toutes les caractéristiques d'une annonce nexity à l'aide des fonction précédente 
def get_nexity(urlpage):
    """
    Extraction des caractéristiques d'un logement d'une annonce du site "nexity" et stockage dans un vecteur.
    
    urlpage : str
        Url d'une annonce "nexity"
    """
    soup = basics.get_page(urlpage)
    appart = nexity.options(soup) + [urlpage]
    appart.insert(0, nexity.localisation(soup)[0])
    appart.insert(1, nexity.localisation(soup)[1])
    appart.insert(2, nexity.price(soup)[0])
    appart.insert(3, nexity.price(soup)[1])
    return appart