# Fonctions pour le site "ORPI"

# a) Récupération du type : appartement ou maison
def get_type(soup):
    text = soup.find_all("span", class_='u-block@sm u-block@md-plus')[0].text
    if (text.find("Appartement") != -1) == True:
        typ = "Appartement"
    elif (text.find("Maison") != -1) == True:
        typ = "Maison"
    return [typ]

# b) Récupération de la ville : Strasbourg et alentour
def get_ville(soup):
    text = soup.find("span", class_='u-h3 u-ml-xs u-text-normal').text
    return [text]

# c) Loyer et Charges
def get_loyer_charges(soup): 
    text = soup.find("ul", class_='u-list-unstyled u-text-xs u-mt-xs u-color-text-grey').find_all('li')
    for i in range(len(text)):
        et = text[i].text
        if "Loyer" in et:
            loyer = float(''.join(re.findall(r'\d', et)))
        if "Provisions" in et:
            prov = float(''.join(re.findall(r'\d', et)))
    return [loyer, prov]

# d) Nombre de pièce et surface
def get_piece(soup):
    text = soup.find_all(class_='u-flex u-flex-cross-center')
    piece = float('nan')
    surface = float('nan')
    for i in range(len(text)):
        if "pièce" in text[i].find("span").text:
            piece = float(re.findall(r'\d+', text[i].find("span").text)[0])
        if "Surface" in text[i].find("span").text:
            surface = float(re.findall(r'\d+', text[i].find("span").text)[0])
    if (piece == 'nan')==True:
        text = soup.find_all(class_='u-block@sm u-block@md-plus')
        text = text[1].text.split()
        for i in range(len(text)):
            if "pièce" in text[i]:
                piece = float(text[i-1])
            if "m2" in text[i]:
                surface = float(text[i-1])
    return [piece , surface]

# e) Caractéristiques spécifiques (Meublé, Ascenseur, Balcon, Terrasse, Cave, Étage)
def get_caracteristiques(soup):
    obj = ["Meublé", "Ascenseur", "Balcon", "Terrasse", "Cave"] # "Etage à rajouter"
    text = soup.find_all(class_='u-flex u-flex-cross-center')
    element = []
    crtqs = [float(0)] * len(obj)
    for i in range(len(text)-1):
        piece = text[i].find("span").text
        element.append(piece)

    for i in range(len(obj)):
        for j in range(len(element)):
            if (obj[i]=="Étage")==True:
                if obj[i] in element[j]:
                    crtqs[i] = float(element[j].split()[1])
                else:
                    crtqs[i] = float("nan")
            else:
                if obj[i] in element[j]:
                    crtqs[i] = float(1)
                    break
    return crtqs

# f) Récupération du terrain et de la place de stationnement

def get_park_and_terrain(soup):
    park = 0
    terrain = 0
    text = soup.find_all(class_='u-flex u-flex-cross-center')
    for i in range(len(text)):
        piece = text[i].find("span").text.split()
        for j in range(len(piece)):
            if ("parking" in piece[j] or "Garage" in piece[j]):
                park = float(1)
                break
        for j in range(len(piece)):
            if ("jardin" in piece[j] or "Terrain" in piece[j]):
                terrain = float(1)
                break
    return [park, terrain]

# g) Récupération du quartier
def get_quartier(soup):
    quartiers = {"meinau" : 1, "neustadt" : 2, 'poteries' : 3, "esplanade" : 4, "petite france" : 5, "cronenbourg" : 6, "koenigshoffen" : 7, "halles" : 8, "neudorf" : 9, "robertsau" : 10, "gare" : 11, "musau" : 12, "orangerie" : 13, "krutenau" : 14, "forêt noire" : 15, 'centre-ville' : 16, "ostwald" : 17, "illkirch-graffenstaden" : 18, "bischheim" : 19, "lingolsheim" : 20, "schiltigheim" : 21, "port du rhin" : 22, "hautepierre":23, "contades":24, "oberhausbergen" : 25}
    key = list(quartiers.keys())
    text = soup.find_all("h2", class_='u-h3')
    if (get_ville(soup) == ["Strasbourg"])==True: # Si la ville est strasbourg, on récupère le quartier
        for i in range(len(text)):
            et = text[i].text
            if "Quartier" in et:
                localisation = re.findall(r'Quartier (.*?) à', et)
                for i in range(len(key)):
                    if (localisation[0].lower().find(key[i]) != -1)==True:
                        q = [key[i].capitalize()]
                        q_num = [float(quartiers.get(key[i]))]
    else: # Si la ville n'est pas strasbourg, le nom du quartier sera le nom de la ville
        for i in range(len(key)):
            if (get_ville(soup)[0].lower().find(key[i]) != -1)==True:
                q_num = [float(quartiers.get(key[i]))]
                q = [key[i].capitalize()]
    return q + q_num

# h) Récupération de la consommation annuelle d'énergie et d'emission de gaz à effet de serre
# Ici on sépare la fonction en 3 cas : Si aucune info sur l'énergie est dispo, si une seule info et dispo et si la 
# consommation et les emissions de GES sont disponibles.
# L'idée ici est de récuperer le vecteur avec les lettres et la consommation dans l'annonce et de regarder si est différent
# de celui de référence.
def get_conso(soup):
    vecteur = ["A", "B", "C", "D", "E", "F", "G"] # Vecteur des classes énergies
    text = soup.find_all("ul", class_='c-dpe')
    
    if (len(text)==0)==True: # Si aucune info est disponible dans l'annonce
        nrj = [float('nan'), float('nan')]
    
    elif (len(text)==1)==True: # Si une seule info est disponible
            et = text[0].text
            resultats = re.findall(r'[A-Za-z]+|\d+|kWh/m2\.an', et)
            for i in range(len(resultats)):
                if (resultats[i] == vecteur[i]) == False:
                    for resultat in resultats:
                        if (resultat == 'kWh') == True:
                            nrj = [float(resultats[i]), float("nan")]
                        elif (resultat == 'kgeqCO') == True:
                            nrj = [float('nan'), float(resultats[i])]
                    break

    elif (len(text)==2)==True:
        for i in range(len(text)): # Si les deux sont disponibles dans l'annonce
            et = text[i].text
            resultats = re.findall(r'[A-Za-z]+|\d+|kWh/m2\.an', et)
            for i in range(len(resultats)):
                if (resultats[i] == vecteur[i]) == False:
                    for resultat in resultats:
                        if (resultat == 'kWh') == True:
                            nrj = float(resultats[i])
                        if (resultat == 'kgeqCO') == True:
                            ges = float(resultats[i])
                    break
                    
        nrj = [nrj, ges]
    return nrj

# Fonction qui nous donne toutes les caractéristiques d'une annonce ORPI à l'aide des fonctions précédentes 
def get_orpi(urlpage):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    soup = get_page(urlpage)
    link = [urlpage]
    appart = get_type(soup) + get_ville(soup) + get_quartier(soup) + get_loyer_charges(soup) + get_piece(soup) + get_caracteristiques(soup) + get_park_and_terrain(soup) + link
    return appart