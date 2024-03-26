# Chargement des packages que nous allons utiliser dans ce script
import random
import re
import seaborn as sns
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import basics_fonctions as basics

# a) Type : appartement ou maison
def typ(soup):
    text = soup.find_all("span", class_='u-block@sm u-block@md-plus')[0].text
    if text.find("Appartement") != -1:
        typ = "Appartement"
    elif text.find("Maison") != -1:
        typ = "Maison"
    return [typ]

# b) Localisation : Ville et quartier
def localisation(soup):
    ville = soup.find("span", class_='u-h3 u-ml-xs u-text-normal').text
    quartiers = ["meinau", "neustadt", 'poteries', "esplanade", "petite france", "cronenbourg", "koenigshoffen", "halles", "neudorf", "robertsau", "gare", "musau", "orangerie", "krutenau", "forêt noire", 'centre-ville', "port du rhin", "hautepierre", "contades"]
    text = soup.find_all("h2", class_='u-h3')
    if ville == "Strasbourg":
        for i in range(len(text)):
            element = text[i].text
            if "Quartier" in element:
                localisation = re.findall(r'Quartier (.*?) à', element)
                for j in range(len(quartiers)):
                    if localisation[0].lower().find(quartiers[j]) != -1:
                        quartier = quartiers[j].capitalize()
    else:
        quartier = ville
    return [ville, quartier]

# c) Loyer, charges et honoraires
def price(soup): 
    text = soup.find("ul", class_='u-list-unstyled u-text-xs u-mt-xs u-color-text-grey').find_all('li')
    honoraires = float('nan')
    for i in range(len(text)):
        element = text[i].text
        if "Loyer" in element:
            loyer = float(''.join(re.findall(r'\d', element)))
        if "Provisions" in element:
            charges = float(''.join(re.findall(r'\d', element)))
        if "Honoraire" in element:
            honoraires = float(''.join(re.findall(r'\d', element)))
    return [loyer, charges, honoraires]

# d) Pièces et surface
def feature(soup):
    text = soup.find_all(class_='u-flex u-flex-cross-center')
    piece = float('nan')
    surface = float('nan')
    for i in range(len(text)):
        if "pièce" in text[i].find("span").text:
            piece = float(re.findall(r'\d+', text[i].find("span").text)[0])
        if "Surface" in text[i].find("span").text:
            surface = float(re.findall(r'\d+', text[i].find("span").text)[0])
    if piece == 'nan' or surface == 'nan':
        text = soup.find_all(class_='u-block@sm u-block@md-plus')[1].text.split()
        for i in range(len(text)):
            if piece == 'nan' and "pièce" in text[i]:
                piece = float(text[i-1])
            if surface == 'nan' and "m2" in text[i]:
                surface = float(text[i-1])
    return [piece, surface]

# e) Caractéristiques
def options(soup):
    variables = ["meublé", "ascenseur", "balcon", "terrasse", "cave", "terrain", "garage"]
    text = soup.find_all(class_='u-flex u-flex-cross-center')
    caracteristiques = list(np.zeros(7, dtype=float))
    for i in range(len(text)-1):
        for j in range(len(variables)):
            if variables[j] in text[i].find("span").text.lower():
                caracteristiques[j] = float(1)
    return caracteristiques

# Fonction qui nous donne toutes les caractéristiques de l'annonce orpi à l'aide des fonction précédente 
def get_orpi(urlpage):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    soup = basics.get_page(urlpage)
    link = [urlpage]
    appart = orpi.typ(soup) + orpi.localisation(soup) + orpi.price(soup) + orpi.feature(soup) + orpi.options(soup) + link
    return appart