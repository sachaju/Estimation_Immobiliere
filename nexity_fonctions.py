# Packages
import random
import re
import seaborn as sns
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import basics_fonctions as basics

# a) Localisation : Ville et quartier
def localisation(soup):
    ville = [soup.find("span", class_='city').text]
    if ville == ["Strasbourg"]:
        quartiers = ["meinau", "neustadt", 'poteries', "esplanade", "petite france", "cronenbourg", "koenigshoffen", "halles", "neudorf", "robertsau", "gare", "musau", "orangerie", "krutenau", "forêt noire", 'centre-ville', "port du rhin", "hautepierre", "contades"]
        text = soup.find("div", class_='description text_body_1 mt-2').text.lower().split()
        quartier = ["nan"]
        for i in range(len(quartiers)):
            for j in range(len(text)):
                if quartiers[i] in text[j]:
                    quartier = [quartiers[i].capitalize()]
                    break
    else:
        quartier = ville
    return ville + quartier

# b) Honoraires
def honoraires(soup):
    text = soup.find("div", class_="block-characteristiques--bareme")
    text = text.text
    text = re.sub(r'\s+', ' ', text)
    hono1 = float(re.findall(r"Honoraires d'organisation de la visite.*?(\d+\.\d+)", text)[0])
    hono2 = float(re.findall(r"Honoraires de réalisation d'état des lieux.*?(\d+)", text)[0])
    honoraires = [hono1 + hono2]
    return honoraires
                               
# c) Meublé
def meuble(soup):
    text = soup.find_all("div", class_='flap flap--not-new')
    if (text == [])==True:
        meuble = [float(0)]
    else:
        text = text[0].text
        if str(text)=='location meublée':
            meuble = [float(1)]
        else:
            meuble = [float(0)]
    return meuble            

# d) caractéristiques : "type", "loyer", "charges /", "pièce(s)", "surface", "ascenseur", "balcon", "terrasse", "cave", "parking" et "terrain"
def options(soup):  
    variables = ["type", "loyer", "charges /", "pièce(s)", "surface", "ascenseur", "balcon", "terrasse", "cave", "parking", "terrain"]
    caracteristiques = list(np.zeros(len(variables), dtype=float))
    text = soup.find_all("div", class_='d-flex align-items-center')
    for i in range(len(text)):
        element = text[i].text.lower()
        for j in range(len(variables)):
            if variables[j] in element:
                caracteristiques[j] = element.split()[len(element.split())-1].capitalize()
                break
    caracteristiques[4] = caracteristiques[4].replace('m²', '')
    for i in [1,2,3,4]:
        caracteristiques[i] = float(caracteristiques[i])
    for j in [5,6,7,8,9,10]:
        if caracteristiques[j] == "Non":
            caracteristiques[j] = float(0)
        else:
            caracteristiques[j] = float(1)
    return caracteristiques

# Fonction qui nous donne toutes les caractéristiques d'une annonce nexity à l'aide des fonction précédente 
def get_nexity(urlpage):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    soup = basics.get_page(urlpage)
    link = [urlpage]
    appart = nexity.options(soup) + link
    appart.insert(1, nexity.localisation(soup)[0])
    appart.insert(2, nexity.localisation(soup)[1])
    appart.insert(5, nexity.honoraires(soup)[0])
    appart.insert(8, nexity.meuble(soup)[0])
    return appart