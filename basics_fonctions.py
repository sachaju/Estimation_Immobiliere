# Ce code regroupe les fonctions globales utiliser dans le scraping des sites immobiliers
# On a : - get_page() : qui permet d'obtenir le HTML d'une page
#        - get_nb_page() : qui permet d'obtenir toutes les pages où il y a des annonces
#        - get_link() : qui permet de récuperer le lien de toutes les annonces disponibles sur un site
#        - get_appart() : qui permet de stocker dans un dataframe les caractéristiques des annonces d'un site
#        - import_data() : qui permet d'importer les données sur les logements

# Chargement des packages que nous allons utiliser dans ce script
import random
import time 
import re
import seaborn as sns
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import orpi_fonctions as orpi
import nexity_fonctions as nexity
import lefigaro_fonctions as lefigaro
import basics_fonctions as basics

# Fonction pour avoir la le code html pour une page internet quelconque
def get_page(urlpage):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    # Timer qui retard l'envoi de requête vers le site pour pas se faire ban
    time.sleep(0.2 + np.random.rand()/10)
    res = requests.get(urlpage, headers = user_agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

def get_pagelink(urlpage):
    # Cette fonction sert à rechercher les différentes pages du site pour obtenir toutes les annonces du site lefigaro
    # L'idée ici est de regarder si la page à un bouton "suivant" pour aller à la prochaine page
    # Quand on a fait toutes les pages qui sont disponibles, link = "VIDE" donc on arrète car il n'y a pas de suivant
    # Et on stocke tous les liens dans "page" et dans ces pages on va récupérer les liens des annonces avec la fonction get_link()
    website = "https://immobilier.lefigaro.fr" 
    link = [] # On initialise un vecteur vide où on va stocker les liens des différences pages
    page = [urlpage] # La première page est celle qu'on a donner dans la fonction get_link()
    while link != "VIDE": # Tant que link n'est pas vide, c'est-à-dire tant qu'on est pas à la dernière page
        soup = basics.get_page(urlpage) 
        text = soup.find_all("a", "router-link-active router-link-exact-active btn-pagination") # Récupération du html
        for i in range(len(text)): # Il y a 2 élements dans "text" : "Précédent" et "Suivant".
            if text[i].text == "Suivant": # On cherche l'element "Suivant"
                link = re.findall('href="(.*?)" ', str(text[i]))[0] # Et on cherche le lien
                urlpage = website + link # On merge le nom du site et la partie du lien spécifique à la page pour avoir le lien complet
                page.append(urlpage) # On ajoute le lien au vecteur "page" pour le stocker
                break
            else:
                link = "VIDE" # Si il n'y a de "Suivant", c'est que c'est la dernière page donc on arrète.
    return page

# Fonction qui nous permet de récupérer le lien des annonces des logements
# Les sites disponibles sont "orpi", "nexity" et "lefigaro"
def get_link(site):
    # On récupère les caractèristiques pour le site 'orpi'
    if (site=='orpi')==True:
        urlpage = 'https://www.orpi.com/location-immobiliere-strasbourg/louer-appartement/' # url
        a = "a" # la balise
        b = 'u-link-unstyled c-overlay__link' # la classe
        website = "https://www.orpi.com" # le lien du site web
        reg = 'href="(.*?)">\n<span' # la regular expression qui encadre notre lien
    # On récupère les caractéristiques pour le site 'nexity'
    if (site=='nexity')==True:
        urlpage = 'https://www.nexity.fr/annonces-immobilieres/location/appartement/tout/strasbourg+67' # url
        a = "div" # la balise
        b = 'product-card-content flex flex-column align-items-start' # la classe
        website = "https://www.nexity.fr" # le lien du site web
        reg = 'href="(.*?)" target' # la regular expression qui encadre notre lien
    
    # On récupère les caractèristiques pour le site 'lefigaro'
    if (site=='lefigaro')==True:
        urlpage = 'https://immobilier.lefigaro.fr/annonces/immobilier-location-appartement-strasbourg+67000.html' # url
        a = "a" # la balise
        b = 'content__link' # la classe
        website = "https://immobilier.lefigaro.fr" # le lien du site web
        reg = 'href="([^"]*)"' # la regular expression qui encadre notre lien
        
        # Comme il y a plusieurs pages sur le site "lefigaro", il faut prendre le lien des annonces pour toutes les pages
        page_link = basics.get_pagelink(urlpage) # On récupère les liens des différentes pages de lefigaro
        links = [] # On initialise le vecteur où on va stocker tous les liens des annonces

        for i in page_link:
            soup = basics.get_page(i)
            annonces = soup.find_all(a, class_= b) # On récupère le html de toutes les annonces sur cette page
            for i in range(len(annonces)):
                text = str(annonces[i]) # On met chaque annonce en chaine de caractère
                link = re.findall(reg, text)[0] # On cherche la regular expression qu'on a définit plus haut
                path = website + link # On regroupe le lien du site et le lien de l'annonce pour avoir le lien complet
                links.append(path) # On l'ajoute à notre vecteur "links"
    
    # Pour ces deux sites, pas besoin car il n'y a qu'une page
    if (site=='nexity' or site=='orpi')==True:
        # On charge la page d'acceuil ou toutes les annonces sont énumérées
        soup = basics.get_page(urlpage) 
        # On recupère les infos dans le html
        annonces = soup.find_all(a, class_= b)
        # On initialise un vecteur vide pour stocker les liens des annonces
        links = []

        for i in range(len(annonces)):
            text = str(annonces[i]) #On met chaque annonce en chaine de caractère
            link = re.findall(reg, text)[0] # On cherche la regular expression qu'on a définit plus haut
            path = website + link # On regroupe le nom du site et le nom de l'annonce
            links.append(path) # On l'ajoute à notre vecteur "links"
        
    return links

# Fonction qui reprend toutes les fonctions précédentes pour faire une fonction qui fait tout !
def get_appart(site):
    links = basics.get_link(site)
    var = ["Type", "Ville", "Quartier", "Loyer", "Charges", "Honoraires", "Pièces", "Surface", "Meublé", "Ascenseur", "Balcon", "Terrasse", "Cave", "Parking", "Terrain", "Liens"]
    data = []
    if (site=="orpi")==True:
        for i in range(len(links)):
            info = orpi.get_orpi(links[i])
            data.append(info)
    if (site=="nexity")==True:
        for i in range(len(links)):
            if (links[i].find("residence_etudiant") != -1)==False:
                info = nexity.get_nexity(links[i])
                data.append(info)
    if (site=="lefigaro")==True:
        for i in range(len(links)):
            info = lefigaro.get_lefigaro(links[i])
            data.append(info)
    data = pd.DataFrame(data, columns=var)
    return data  

def import_data(site):
    t = time.time()
    if site != "all":
        dt = basics.get_appart(site)
    else:
        dt = pd.concat([basics.get_appart("orpi"), basics.get_appart("nexity"), basics.get_appart("lefigaro")], ignore_index=True)
    dt = dt.dropna(subset=["Loyer", "Surface", 'Charges', 'Pièces', 'Terrain', 'Meublé', 'Ascenseur', 'Balcon', 'Terrasse','Cave','Parking'])
    dt = dt.reset_index(drop=True)
    n=len(dt)-1
    val_double_i = []
    val_double_j = []
    for i in range(0,n):
        for j in range(i+1,n+1):
            if (dt.iloc[i, [1,2,4,5,7,8]].tolist() == dt.iloc[j, [1,2,4,5,7,8]].tolist())==True:
                val_double_i.append(i)
                val_double_j.append(j)
    val_double = []
    for i in range(len(val_double_i)):
        if dt.iloc[val_double_i[i],6] > dt.iloc[val_double_j[i],6]:
            val_double.append(val_double_i[i])
        elif dt.iloc[val_double_i[i],6] < dt.iloc[val_double_j[i],6] or dt.iloc[val_double_i[i],6] == dt.iloc[val_double_j[i],6]:
            val_double.append(val_double_j[i])
        elif dt.iloc[val_double_i[i],6] == 'nan' and dt.iloc[val_double_j[i],6] != 'nan':
            val_double.append(val_double_i[i])
        elif dt.iloc[val_double_i[i],6] != 'nan' and dt.iloc[val_double_j[i],6] == 'nan':
            val_double.append(val_double_j[i])
        else:
            val_double.append(val_double_j[i])   
    dt = dt.drop(list(np.unique(val_double)))
    dt = dt.reset_index(drop=True)
    print((time.time() - t)/60)
    return dt