# Packages
import random
import re
import seaborn as sns
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import basics_fonctions as basics

# a) Type
def typ(soup):
    text = soup.find_all('h1')[0].text.lower()
    if 'appartement' in text or 'studio' in text or 'location' in text:
        typ=['Appartement']
    elif 'maison' in text:
        typ=['Maison']
    return typ

# b) localisation : ville et quartier
def localisation(soup):
    ville = [re.search(r'à (\w+)', soup.find_all('h1')[0].text.lower()).group(1).capitalize()]
    quartiers = ["meinau", "neustadt", 'poteries', "esplanade", "petite france", "cronenbourg", "koenigshoffen", "halles", "neudorf", "robertsau", "gare", "musau", "orangerie", "krutenau", "forêt noire", 'centre-ville', "port du rhin", "hautepierre", "contades"]
    text = soup.find_all("p", class_='truncated-description')[0].text.lower()
    quartier = ["nan"]
    if ville==["Strasbourg"]:
        for i in range(len(quartiers)):
            if text.find(quartiers[i]) != -1:
                quartier = [quartiers[i].capitalize()]
    else:    
        for i in range(len(quartiers)):
                quartier = [ville]
    return ville + quartier

# c) Loyer et charges
def price(soup):
    loyer = soup.find_all('span', class_='price')[0].text
    loyer = float(re.sub(r'[^\d.]', '', loyer))
    charges = soup.find_all('span', class_='about-price-fees-label')
    if (charges == [])==True:
        charges = 0
    else:
        charges = charges[0].text
        charges = float(re.search(r'\d+', charges).group())
    if "CC" in (soup.find_all('span', class_='price')[0].text):
        loyer = loyer - charges
    return [loyer, charges]

# d) Honoraires
def honoraires(soup):
    text = soup.find_all('li', class_='item-about-price')
    honoraires = [float('nan')]
    for i in range(len(text)):
        if "honoraires" in text[i].text.lower():
            if "non communiqué" in text[i].text.lower():
                honoraires = [float('nan')]
            else:
                honoraires = [float(re.search(r'\b\d+\b',text[2].text.lower())[0])]
    return honoraires

# e) Pièces, surface
def feature(soup):
    text= soup.find_all('span', class_='feature')
    for i in range(len(text)):
        element = text[i].text.split()
        if "pièces" in element or 'pièce' in element:
            piece = [float(re.match(r'([\d.]+)', element[0]).group())]
        if "surface" in element:
            surface = [float(re.match(r'([\d.]+)', element[0]).group())]
    return piece + surface

# f) Meublé
def meuble(soup):
    text = soup.find_all("p", class_='truncated-description')[0].text.lower()
    if "meublé" in text:
        meuble = [float(1)]
    else:
        meuble = [float(0)]
    return meuble

# g) Caractéristiques : Ascenseur, "balcon", "terrasse", "cave", "parking" et "jardin"
def options(soup):
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
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    soup = basics.get_page(urlpage)
    link = [urlpage]
    appart = lefigaro.typ(soup) + lefigaro.localisation(soup) + lefigaro.price(soup) + lefigaro.honoraires(soup) + lefigaro.feature(soup) + lefigaro.meuble(soup) + lefigaro.options(soup) + link
    return appart