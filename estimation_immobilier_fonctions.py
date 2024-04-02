import pandas as pd
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
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
                  "Avez-vous une place de stationnement (parking ou garage) ?" : "",
                  }
    
    key = list(Information.keys())
    print("Renseignement des caractéristiques du logement :\n")

    # Affichage de la demande d'information
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

    # importation des données des logements
    dt = basics.data_immo("all")    
    x=dt[["Surface", 'Pièces', 'Terrain', 'Ascenseur', 'Balcon', 'Terrasse', 'Cave', 'Parking']]
    y=dt["Prix"]
    
    # Transformation des variables d'inforamtion de text en boolean et stockage dans X
    X = []
    for i in range(len(key)):
        if (Information.get(key[i])=="Oui")==True:
            info = 1
        elif (Information.get(key[i])=="Non")==True:
            info = 0
        else :
            info = Information.get(key[i])
        X.append(info)
    X = pd.DataFrame([X], columns=x.columns)
    
    # Entrainement du modèle knn
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(x,y)
    distances, indices = model.kneighbors(X)
    
    # Estimation du prix
    prix = []
    for i in range(len(indices[0])):    
        obs = dt.iloc[indices[0][i]]["Prix"]
        prix.append(obs)
    prix = np.array(prix)
    z = distances.sum()- distances[0]
    sum_z = z.sum()
    pond = z/sum_z
    estimation = (prix*pond).sum()
    
    # Intervalle de confiance
    lower_bound = (prix*pond).sum() -  norm.ppf((1.95) / 2) * (np.std(prix) / np.sqrt(len(prix)))
    upper_bound = (prix*pond).sum() + norm.ppf((1.95) / 2) * (np.std(prix) / np.sqrt(len(prix)))
    
    # Affichage des résultats de la fonction
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
                  "Combien de pièces souhaitez-vous ?" : "",        
                  "Souhaitez-vous du terrain ?" : "",
                  "Souhaitez-vous un ascenseur ?" : "", 
                  "Souhaitez-vous un balcon ?" : "",   
                  "Souhaitez-vous une terrasse ?" : "", 
                  "Souhaitez-vous une cave ?" : "",   
                  "Souhaitez-vous une place de statonnement (parking ou garage) ?" : "",
                  }
    
    key = list(Information.keys())
    print("Renseignement des caractéristiques souhaitées :\n")
    
    # Affichage de la demande d'information
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
    
    # importation des données des logements
    dt = basics.data_immo("all")
    x=dt[["Prix", "Surface", 'Pièces', 'Terrain', 'Ascenseur', 'Balcon', 'Terrasse','Cave','Parking']]
    y=dt["Liens"]
    
    # Transformation des variables d'inforamtion de text en boolean et stockage dans X
    X = []
    for i in range(len(key)):
        if (Information.get(key[i])=="Oui")==True:
            info = 1
        elif (Information.get(key[i])=="Non")==True:
            info = 0
        else :
            info = Information.get(key[i])
        X.append(info)
    X = pd.DataFrame([X], columns=x.columns)
    
    # Entrainement du modèle knn
    model = KNeighborsClassifier(n_neighbors=4)
    model.fit(x,y)
    distances, indices = model.kneighbors(X)
    
    # Affichage des résultats de la fonction
    resultats = dt.iloc[indices[0]][["Liens", "Prix", "Surface", "Pièces", "Quartier", "Honoraires"]]
    for i in range(len(resultats)):
        if resultats.iloc[i][4]=="nan":
            quart = "Non renseigné"
        else:
            quart = resultats.iloc[i][4]
        print("\nAnnonce",i+1,":")
        print("Quartier : ", quart)
        print("Prix : ", int(resultats.iloc[i][1]), "€\n" "Honoraires : ", resultats.iloc[i][5], "€\n" "Surface : ", resultats.iloc[i][2], "m2","\n" "Pièces : ", int(resultats.iloc[i][3]),"\n" "Lien : ", resultats.iloc[i][0])