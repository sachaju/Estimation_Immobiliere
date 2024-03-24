# Fonctions pour les estimations de notre modèle à l'aide de l'algorithme knn

# Fonctions de l'estimations du prix d'un appartement selon ses caractéristiques
def get_estimation(Information):
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
        
