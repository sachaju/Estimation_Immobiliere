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
def get_estimation(Information):
    
    Information = {"Loyer" : 1000,      # En €
              "Surface" : 80,      # En m²
              "Charges": 100,       # En €
              "Pièces" : 4,        # En nombre
              "Terrain" : 0,       # En m²
              "Meublé" : "Non",    # "Oui" ou "Non"
              "Ascenseur" : "Non", # "Oui" ou "Non"
              "Balcon" : "Oui",    # "Oui" ou "Non"
              "Terrasse" : "Non",  # "Oui" ou "Non"
              "Cave" : "Non",      # "Oui" ou "Non"
              "Parking" : "Oui",   # "Oui" ou "Non"
              }
    
    dt = basics.import_data("all")
    
    a=dt[["Surface", 'Charges', 'Pièces', 'Étage', 'Terrain', 'Meublé', 'Ascenseur', 'Balcon', 'Terrasse','Cave', 'Parking']]
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
    distances, indices = model.kneighbors([X[1:]])
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
    
# Obtenir 4 annonces proches d'un logement donné
def get_annonce(Information):
    
    Information = {"Loyer" : 1000,      # En €
              "Surface" : 80,      # En m²
              "Charges": 100,       # En €
              "Pièces" : 4,        # En nombre
              "Terrain" : 0,       # En m²
              "Meublé" : "Non",    # "Oui" ou "Non"
              "Ascenseur" : "Non", # "Oui" ou "Non"
              "Balcon" : "Oui",    # "Oui" ou "Non"
              "Terrasse" : "Non",  # "Oui" ou "Non"
              "Cave" : "Non",      # "Oui" ou "Non"
              "Parking" : "Oui",   # "Oui" ou "Non"
              }
    
    dt = basics.import_data("all")
    
    a=dt[["Loyer", "Surface", 'Charges', 'Pièces', 'Étage', 'Terrain', 'Meublé', 'Ascenseur', 'Balcon', 'Terrasse','Cave','Parking']]
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
        