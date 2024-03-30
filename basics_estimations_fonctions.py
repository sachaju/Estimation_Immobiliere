import random
import re
import seaborn as sns
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from scipy.spatial import cKDTree
from scipy.stats import norm
import functools
import time
import basics_estimations_fonctions as basics
import orpi_fonctions as orpi
import nexity_fonctions as nexity
import lefigaro_fonctions as lefigaro

# Fonction qui permet de récuperer le code html d'un page internet
# ATTENTION : IL FAUT MODIFIER L'USER AGENT !!!!!!

# Décorateur pour rajouter un cache à la fonction get_page.
# Ceci est fait pour gagner du temps et ne pas avoir à charger plusieurs fois les pages quand on utilise plusieurs fois la fonction finale
@functools.cache
def get_page(urlpage): 
    """
    Récupération du HTML d'un site internet via Beautifulsoup
    """
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    time.sleep(0.2 + np.random.rand()/10) # Retarder le téléchargement pour pas se faire ban
    res = requests.get(urlpage, headers = user_agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def get_links_page_lefigaro(urlpage):
    """
    Stockage des url des différentes pages du sites "lefigaro" dans un vecteur où sont stockés les annonces
    
    Tant que la page possède un bouton suivant à la fin de la liste des annonces, on cherche l'url de la page suivante et on la stocke dans le vecteur `pages`
    """
    website = "https://immobilier.lefigaro.fr" 
    link = None
    pages = [urlpage]
    while link != "VIDE":
        soup = basics.get_page(urlpage) 
        text = soup.find_all("a", "router-link-active router-link-exact-active btn-pagination") # Récupération du html de la page suivante
        for i in range(len(text)): # Il y a 2 élements dans "text" : "Précédent" et "Suivant".
            if text[i].text == "Suivant": # On cherche l'élement "Suivant"
                link = text[i].get("href") # Et on cherche le lien qui est après "href="
                urlpage = website + link # On merge le nom du site et la partie du lien spécifique à la page pour avoir le lien complet
                pages.append(urlpage) # On ajoute le lien au vecteur "page" pour le stocker
                break
            else:
                link = "VIDE"
    return pages

def get_link(site):
    """
    Récupération des liens html de toutes les annonces d'un site
    
    site : str  
        valeur : "orpi", "nexity" ou "lefigaro"
    """
    links = []
    # Récupération des liens pour 'orpi'
    if (site=='orpi')==True:
        soup = basics.get_page('https://www.orpi.com/annonces-immobilieres-strasbourg/vente-appartement/')
        annonces = soup.find_all("a", class_= 'u-link-unstyled c-overlay__link')
        for annonce in annonces:
            link = annonce.get("href")
            path = "https://www.orpi.com" + link 
            links.append(path)
        
    # Récupération des liens pour 'nexity'
    if (site=='nexity')==True:
        soup = basics.get_page('https://www.nexity.fr/annonces-immobilieres/achat-vente/appartement/tout/strasbourg+67')
        annonces = soup.find_all("h2", class_= 'informations')
        for annonce in annonces:
            link = annonce.a.get("href")
            if "neuf" in link: # Exclusion des "neuf" car il s'agit de projet de construction
                continue
            path = "https://www.nexity.fr" + link # 
            links.append(path)
    
    # Récupération des liens pour 'lefigaro'
    if (site=='lefigaro')==True:
        
        # Comme il y a plusieurs pages sur le site "lefigaro", il faut prendre le lien des annonces pour toutes les pages
        page_link = basics.get_links_page_lefigaro("https://immobilier.lefigaro.fr/annonces/immobilier-vente-appartement-strasbourg+67000.html")# On récupère les liens des différentes pages de lefigaro

        for page in page_link:
            soup = basics.get_page(page)
            annonces = soup.find_all("a", class_= 'content__link')
            for annonce in annonces: # Pour chaque annonce, on récupère le lien html
                link = annonce.get("href")
                if "https" not in link: # exclusion des autres sites proposés par lefigaro
                    path = "https://immobilier.lefigaro.fr" + link # On regroupe le lien du site et le lien de l'annonce pour avoir le lien complet
                    links.append(path) # On l'ajoute à notre vecteur "links"
        
    return np.unique(links)

def get_appart(site):
    """
    Création d'un data frame qui contient les caractéristiques des annonces d'un site immobilier spécifique.
    
    site : str
        Valeur : "orpi", "nexity" ou "lefigaro"
    """
    links = basics.get_link(site)
    var = ["Ville", "Quartier", "Prix", "Honoraires", "Pièces", "Surface", "Ascenseur", "Balcon", "Terrasse", "Cave", "Parking", "Terrain", "Liens"]
    data = []
    z=0 # Initialisation d'un compteur
    if (site=="orpi")==True:
        for i in range(len(links)):
            z+=1
            print("Site : Orpi - Chargement : ", round((z/len(links))*100), "%", end="\r") # Affichage du compteur pour indiquer l'évolution du chargement des données
            info = orpi.get_orpi(links[i]) # On récupère le vecteur des caractéristiques d'un logement à partir des liens que nous avons récupérés
            data.append(info) # On ajoute notre observation au vecteur data qui regroupe toutes les observations
    if (site=="nexity")==True:
        for i in range(len(links)):
            z+=1
            print("Site : Nexity - Chargement : ", round((z/len(links))*100), "%", end="\r")
            info = nexity.get_nexity(links[i])
            data.append(info)
    if (site=="lefigaro")==True:
        for i in range(len(links)):
            z+=1
            print("Site : Lefigaro - Chargement : ", round((z/len(links))*100), "%", end="\r")
            info = lefigaro.get_lefigaro(links[i])
            data.append(info)
    data = pd.DataFrame(data, columns=var)
    return data

def data_immo(site):
    """
    Création d'un data frame qui contient les caractéristiques de toutes les annonces pour les sites "orpi", "nexity" et "lefigaro" avec traitement des valeurs manquantes et des doublons.
    
    site : str
        Valeur : "orpi", "nexity" ou "lefigaro"
    """
    t = time.time()
    print("Extraction et chargement des données...\n")
    if site != "all":
        dt = basics.get_appart(site)
    else:
        dt = pd.concat([basics.get_appart("orpi"), basics.get_appart("nexity"), basics.get_appart("lefigaro")], ignore_index=True)
    
    # Traitement des valeurs manquantes
    dt = dt.dropna(subset=["Prix", "Surface", 'Pièces', 'Terrain', 'Ascenseur', 'Balcon', 'Terrasse','Cave','Parking'])
    dt = dt.reset_index(drop=True)
    
    #Traitement des valeurs doubles
    doublons = []
    for i in range(len(dt)):
        if dt[["Prix", "Pièces", "Surface"]].duplicated()[i] == True:
            doublons.append(i)
    for j in range(len(doublons)):
        dt = dt.drop(doublons[j])
    dt = dt.reset_index(drop=True)
    print("Extraction terminée en ", round((time.time() - t)/60, 2), "minutes")
    return dt

