import re

import numpy as np

import orpi_fonctions as orpi
import nexity_fonctions as nexity
import lefigaro_fonctions as lefigaro
import basics_estimations_fonctions as basics

# a) Localisation : Ville et Quartier
def localisation(soup):
    """
    Récupération de la ville et du quartier pour un logement d'une annonce du site "orpi".
    """
    ville = soup.find("span", class_='u-h3 u-ml-xs u-text-normal').text
    quartiers = ["meinau", "neustadt", 'poteries', "esplanade", "petite france", "cronenbourg", "koenigshoffen", "halles", "neudorf", "robertsau", "gare", "musau", "orangerie", "krutenau", "forêt noire", 'centre-ville', "port du rhin", "hautepierre", "contades", "tribunal", "neuhof", "montagne verte"]
    text = soup.find_all("h2", class_='u-h3')
    if ville == "Strasbourg":
        for i in range(len(text)):
            if "Quartier" in text[i].text:
                quartier = re.findall(r'Quartier (.*?) à', text[i].text)
                for j in range(len(quartiers)):
                    if quartier[0].lower().find(quartiers[j]) != -1:
                        quartier = quartiers[j].capitalize()
    else:
        quartier = ville
    return [ville, quartier]

# b) Prix et Honoraires
def price(soup): 
    """
    Récupération du prix et du montant des honoraires pour un logement d'une annonce "orpi".
    """
    prix = float(soup.find("span", class_='u-h1 u-color-primary').text.replace('\xa0', '').replace('€', ''))
    text = soup.find("ul", class_='u-list-unstyled u-text-xs u-mt-xs u-color-text-grey').find_all('li')
    honoraires = float('nan')
    for i in range(len(text)):
        element = text[i].text
        if "Honoraire" in element:
            if "acquéreur" in element:
                honoraires = prix * float(re.search(r'\b\d+(?:\.\d+)?', element).group(0))/100
            else:
                honoraires = 0
    return [prix, honoraires]

# c) Pièces et Surface
def feature(soup):
    """
    Récupération de la surface (nombre de m²) et du nombre de pièce d'un logement d'une annonce "orpi".
    """
    text = soup.find_all(class_='u-flex u-flex-cross-center')
    piece = float('nan')
    surface = float('nan')
    for i in range(len(text)):
        if "pièce" in text[i].find("span").text:
            piece = float(re.findall(r'\d+', text[i].find("span").text)[0])
        if "Surface" in text[i].find("span").text:
            surface = float(re.search(r'\d+[\.,]?\d*', text[i].find("span").text).group(0).replace(',', '.'))
    if piece == 'nan' or surface == 'nan': # Si piece et surface sont toujours "nan", les caractéristiques sont peut être à un autre endroit
        text = soup.find_all(class_='u-block@sm u-block@md-plus')[1].text.split()
        for i in range(len(text)):
            if piece == 'nan' and "pièce" in text[i]:
                piece = float(text[i-1])
            if surface == 'nan' and "m2" in text[i]:
                surface = float(text[i-1])
    return [piece, surface]

# d) Caractéristiques
def options(soup):
    """
    Récupération des options disponibles pour un logement d'une annonce "orpi".
    Options : "Ascenseur", "Balcon", "Terrasse", "Cave", "Garage", "Terrain".
    """
    variables = ["ascenseur", "balcon", "terrasse", "cave", "garage", "terrain"]
    text = soup.find_all(class_='u-flex u-flex-cross-center')
    caracteristiques = list(np.zeros(len(variables), dtype=float))
    for i in range(len(text)-1):
        for j in range(len(variables)):
            if variables[j] in text[i].find("span").text.lower():
                caracteristiques[j] = float(1)
    return caracteristiques

# Fonction qui nous donne toutes les caractéristiques d'une annonce orpi à l'aide des fonctions précédentes 
def get_orpi(urlpage):
    """
    Extraction des caractéristiques d'un logement d'une annonce du site "orpi" et stockage dans un vecteur.
    
    urlpage : str
        Url d'une annonce "orpi"
    """
    soup = basics.get_page(urlpage)
    appart = orpi.localisation(soup) + orpi.price(soup) + orpi.feature(soup) + orpi.options(soup) + [urlpage]
    return appart