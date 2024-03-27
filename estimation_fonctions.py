# Fonctions pour les estimations de notre modèle à l'aide de l'algorithme knn

# Chargement des packages que nous allons utiliser dans ce script
import time 
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
import basics_fonctions as basics
import orpi_fonctions as orpi
import nexity_fonctions as nexity
import lefigaro_fonctions as lefigaro

# Fonctions de l'estimations du prix d'un appartement selon ses caractéristiques
def get_estimation():
    
    Information = {"Surface" : "",      # En m²
                  "Charges": "",       # En €
                  "Pièces" : "",        # En nombre
                  "Terrain" : "",       # En m²
                  "Meublé" : "",    # "Oui" ou "Non"
                  "Ascenseur" : "", # "Oui" ou "Non"
                  "Balcon" : "",    # "Oui" ou "Non"
                  "Terrasse" : "",  # "Oui" ou "Non"
                  "Cave" : "",      # "Oui" ou "Non"
                  "Parking" : "",   # "Oui" ou "Non"
                  }
    key = list(Information.keys())
    for i in range(len(Information)):
        print(key[i], ":")
        element = input().lower()
        if key[i] == "Loyer" or key[i] == "Surface" or key[i] =="Charges" or key[i] =="Pièces":
            while element.isnumeric() == False:
                if element.isnumeric() == False:
                    print("Erreur : Veuillez insérer une valeur numérique")
                    element = input()
            element = float(element)
        else:
            while element != "oui" and element != "non":
                if element != "oui" and element != "non":
                    print("Erreur : Veuillez indiquer si vous souhaitez cette caractéristique ou non\nRéponses acceptées : Oui ou Non")
                    element = input().lower()
            element = element.capitalize()
        Information[list(Information.keys())[i]]=element
        
    dt=basics.import_data("all")
    
    a=dt[["Surface", 'Charges', 'Pièces', 'Terrain', 'Meublé', 'Ascenseur', 'Balcon', 'Terrasse','Cave', 'Parking']]
    b=dt["Loyer"]
    
    key = list(Information.keys())
    
    X = []
    for i in range(len(key)):
        if (Information.get(key[i])=="Oui")==True:
            ad = 1
        elif (Information.get(key[i])=="Non")==True:
            ad = 0
        else :
            ad = Information.get(key[i])
        X.append(ad)
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(a,b)
    distances, indices = model.kneighbors([X])
    loy = []
    for i in range(len(indices[0])):    
        obs = dt.iloc[indices[0][i]]["Loyer"]
        loy.append(obs)
    loy = np.array(loy)
    z = distances.sum()- distances[0]
    sum_z = z.sum()
    pond = z/sum_z
    estimation = (loy*pond).sum()
    # Intervalle de confiance
    lower_bound = (loy*pond).sum() -  norm.ppf((1.95) / 2) * (np.std(loy) / np.sqrt(len(loy)))
    upper_bound = (loy*pond).sum() + norm.ppf((1.95) / 2) * (np.std(loy) / np.sqrt(len(loy)))
    IC = [int(lower_bound.round()), int(upper_bound.round())]
    print("Estimation du prix : ", estimation.round(), "€")
    print("Interval de confiance du prix : ", IC)
    
def get_annonce():
    Information = {"Loyer" : "",      # En €
              "Surface" : "",      # En m²
              "Charges": "",       # En €
              "Pièces" : "",        # En nombre
              "Terrain" : "",       # En m²
              "Meublé" : "",    # "Oui" ou "Non"
              "Ascenseur" : "", # "Oui" ou "Non"
              "Balcon" : "",    # "Oui" ou "Non"
              "Terrasse" : "",  # "Oui" ou "Non"
              "Cave" : "",      # "Oui" ou "Non"
              "Parking" : "",   # "Oui" ou "Non"
              }
    
    key = list(Information.keys())
    for i in range(len(Information)):
        print(key[i], ":")
        element = input().lower()
        if key[i] == "Loyer" or key[i] == "Surface" or key[i] =="Charges" or key[i] =="Pièces":
            while element.isnumeric() == False:
                if element.isnumeric() == False:
                    print("Erreur : Veuillez insérer une valeur numérique")
                    element = input()
            element = float(element)
        else:
            while element != "oui" and element != "non":
                if element != "oui" and element != "non":
                    print("Erreur : Veuillez indiquer si vous souhaitez cette caractéristique ou non\nRéponses acceptées : Oui ou Non")
                    element = input().lower()
            element = element.capitalize()
        Information[list(Information.keys())[i]]=element
    dt=basics.import_data("all")
    a=dt[["Loyer", "Surface", 'Charges', 'Pièces', 'Terrain', 'Meublé', 'Ascenseur', 'Balcon', 'Terrasse','Cave','Parking']]
    b=dt["Liens"]
    key = list(Information.keys())
    X = []
    for i in range(len(key)):
        if (Information.get(key[i])=="Oui")==True:
            ad = 1
        elif (Information.get(key[i])=="Non")==True:
            ad = 0
        else :
            ad = Information.get(key[i])
        X.append(ad)
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(a,b)
    distances, indices = model.kneighbors([X])
    la = dt.iloc[indices[0]][["Liens", "Loyer", "Surface", "Pièces", "Quartier"]]
    


    for i in range(len(la)):
        if la.iloc[i][4]=="nan":
            quart = "Non renseigné"
        else:
            quart = la.iloc[i][4]
        print("Annonce",i+1,":")
        print("Quartier : ", quart)
        print("Loyer : ", int(la.iloc[i][1]), "€\n" "Surface : ", la.iloc[i][2], "m2","\n" "Pièces : ", int(la.iloc[i][3]),"\n" "Lien : ", la.iloc[i][0])
        print("\n")
        