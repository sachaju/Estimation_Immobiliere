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
import basics_estimations_fonctions as basics
import orpi_fonctions as orpi
import nexity_fonctions as nexity
import lefigaro_fonctions as lefigaro

def estimation():
    """
    Fonctions qui permet d'obtenir une estimation d'un bien immobilier selon des caractéristiques spécifiées.
    """
    # Demandes informations
    Information = {"Quelle est la surface en m² de votre bien" : "",  
                  "Nombre de pièces" : "",        
                  "Avez-vous du terrain ?" : "",
                  "Avez-vous un ascenseur ?" : "", 
                  "Avez-vous un balcon ?" : "",   
                  "Avez-vous une terrasse ?" : "", 
                  "Avez-vous une cave ?" : "",   
                  "Avez-vous une place de statonnement (parking ou garage) ?" : "",
                  }
    
    key = list(Information.keys())
    print("Demande d'informations :\n")

    for i in range(len(Information)):
        print(key[i], ":")
        element = input().lower()
        if "prix" in key[i] or "surface" in key[i] or "pièces" in key[i]:
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

    dt = basics.data_immo("all")    
    a=dt[["Surface", 'Pièces', 'Terrain', 'Ascenseur', 'Balcon', 'Terrasse', 'Cave', 'Parking']]
    b=dt["Prix"]
    
    X = []
    for i in range(len(key)):
        if (Information.get(key[i])=="Oui")==True:
            ad = 1
        elif (Information.get(key[i])=="Non")==True:
            ad = 0
        else :
            ad = Information.get(key[i])
        X.append(ad)
    X = pd.DataFrame([X], columns=a.columns)
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(a,b)
    distances, indices = model.kneighbors(X)
    
    loy = []
    for i in range(len(indices[0])):    
        obs = dt.iloc[indices[0][i]]["Prix"]
        loy.append(obs)
    loy = np.array(loy)
    z = distances.sum()- distances[0]
    sum_z = z.sum()
    pond = z/sum_z
    estimation = (loy*pond).sum()
    # Intervalle de confiance
    lower_bound = (loy*pond).sum() -  norm.ppf((1.95) / 2) * (np.std(loy) / np.sqrt(len(loy)))
    upper_bound = (loy*pond).sum() + norm.ppf((1.95) / 2) * (np.std(loy) / np.sqrt(len(loy)))
    IC = [lower_bound.round(), upper_bound.round()]
    print("")
    print("Estimation du prix : ", "{:,}".format(estimation.round()).replace(","," "), "€")
    print("Interval de confiance du prix : [","{:,}".format(lower_bound.round()).replace(","," "), "€", ";","{:,}".format(upper_bound.round()).replace(","," "), "€", "]")     
        
def annonces():
    """
    Fonctions qui permet d'obtenir une liste d'annonces selon des caractéristiques spécifiées.
    """
    # Demandes informations
    Information ={"Quel est le prix que vous visez ?" : "",
                  "Quelle surface souhaitez-vous ? (en m²)" : "",  
                  "Combien de pièces souhiatez-vous ?" : "",        
                  "Souhaitez-vous du terrain ?" : "",
                  "Souhaitez-vous un ascenseur ?" : "", 
                  "Souhaitez-vous un balcon ?" : "",   
                  "Souhaitez-vous une terrasse ?" : "", 
                  "Souhaitez-vous une cave ?" : "",   
                  "Souhaitez-vous une place de statonnement (parking ou garage) ?" : "",
                  }
    
    key = list(Information.keys())
    print("Demande d'informations :\n")

    for i in range(len(Information)):
        print(key[i], ":")
        element = input().lower()
        if "prix" in key[i] or "surface" in key[i] or "pièces" in key[i]:
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

    dt = basics.data_immo("all")     
    a=dt[["Prix", "Surface", 'Pièces', 'Terrain', 'Ascenseur', 'Balcon', 'Terrasse','Cave','Parking']]
    b=dt["Liens"]
    
    X = []
    for i in range(len(key)):
        if (Information.get(key[i])=="Oui")==True:
            ad = 1
        elif (Information.get(key[i])=="Non")==True:
            ad = 0
        else :
            ad = Information.get(key[i])
        X.append(ad)
    X = pd.DataFrame([X], columns=a.columns)
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(a,b)
    distances, indices = model.kneighbors(X)
    
    la = dt.iloc[indices[0]][["Liens", "Prix", "Surface", "Pièces", "Quartier", "Honoraires"]]

    for i in range(len(la)):
        if la.iloc[i][4]=="nan":
            quart = "Non renseigné"
        else:
            quart = la.iloc[i][4]
        print("\nAnnonce",i+1,":")
        print("Quartier : ", quart)
        print("Prix : ", int(la.iloc[i][1]), "€\n" "Honoraires : ", la.iloc[i][5], "€\n" "Surface : ", la.iloc[i][2], "m2","\n" "Pièces : ", int(la.iloc[i][3]),"\n" "Lien : ", la.iloc[i][0])