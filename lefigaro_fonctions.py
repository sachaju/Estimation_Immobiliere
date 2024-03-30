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

# a) localisation : ville et quartier
def localisation(soup):
    """
    Récupération de la ville et du quartier pour un logement d'une annonce du site "lefigaro".
    """
    ville = re.search(r'à (\w+)', soup.find_all('h1')[0].text.lower()).group(1).capitalize()
    quartiers = ["meinau", "neustadt", 'poteries', "esplanade", "petite france", "cronenbourg", "koenigshoffen", "halles", "neudorf", "robertsau", "gare", "musau", "orangerie", "krutenau", "forêt noire", 'centre-ville', "port du rhin", "hautepierre", "contades", "tribunal", "neuhof", "montagne verte"]
    text = soup.find_all("p", class_='truncated-description')[0].text.lower()
    quartier = "nan"
    if ville=="Strasbourg":
        for i in range(len(quartiers)):
            if text.find(quartiers[i]) != -1:
                quartier = quartiers[i].capitalize()
    else:    
        quartier = ville
    return [ville, quartier]

# b) Loyer et charges
def price(soup):
    """
    Récupération du prix et du montant des honoraires pour un logement d'une annonce "lefigaro".
    """
    price = float(soup.find_all('div', class_='classified-price-per-m2')[0].find("strong").text.replace(" €", "").replace(" ", ""))
    text = soup.find_all('li', class_='item-about-price')
    honoraires = float("nan")
    for i in range(len(text)):
        if "honoraires" in text[i].text.lower():
            if "vendeur" in text[i].text.lower():
                honoraires = float(0)
                break
            elif "non communiqué" in text[i].text.lower():
                honoraires = float("nan")
                break
            else:
                honoraires = price * float(re.search(r'\b\d+(?:\.\d+)?', text[i].text.lower()).group(0))/100
                break
    return [price, honoraires]

# c) Pièces, surface
def feature(soup):
    """
    Récupération de la surface (nombre de m²) et du nombre de pièce d'un logement d'une annonce "lefigaro".
    """
    piece = float("nan")
    surface = float("nan")
    text= soup.find_all('span', class_='feature')
    for i in range(len(text)):
        element = text[i].text.split()
        if "pièces" in element or 'pièce' in element:
            piece = float(re.match(r'([\d.]+)', element[0]).group())
        if "surface" in element:
            surface = float(re.match(r'([\d.]+)', element[0]).group())
    return [piece, surface]

# d) Caractéristiques : Ascenseur, "balcon", "terrasse", "cave", "parking" et "jardin"
def options(soup):
    """
    Récupération des options disponibles pour un logement d'une annonce "lefigaro".
    Options : "Ascenseur", "Balcon", "Terrasse", "Cave", "Garage", "Terrain".
    """
    variables = ["ascenseur", "balcon", "terrasse", "cave", "parking", "jardin"]
    caracteristiques = list(np.zeros(len(variables), dtype=float))
    text = soup.find_all("li", class_='options')
    if text != []:
        for i in range(len(text)):
            for j in range(len(variables)):
                if variables[j] == text[i].text.lower():
                    caracteristiques[j] = float(1)
    return caracteristiques

def get_lefigaro(urlpage):
    """
    Extraction des caractéristiques d'un logement d'une annonce du site "lefigaro" et stockage dans un vecteur.
    
    urlpage : str
        Url d'une annonce "lefigaro"
    """
    soup = basics.get_page(urlpage)
    appart = lefigaro.localisation(soup) + lefigaro.price(soup) + lefigaro.feature(soup) + lefigaro.options(soup) + [urlpage]
    return appart