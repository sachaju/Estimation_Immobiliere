# Fonctions pour le site "NEXITY"

# a) Récupération de la ville
def get_ville_nexity(soup):
    text = soup.find("span", class_='city').text
    return [text]

# b) Récupération du quartier
# Sur Nexity, on a pas accès à la variable quartier, on doit donc regarder dans le texte de description si les noms de 
# quartier ci dessous sont évoqués.
def get_quartier_nexity(soup):
    quartiers = {"meinau" : 1, "neustadt" : 2, 'poteries' : 3, "esplanade" : 4, "petite france" : 5, "cronenbourg" : 6, "koenigshoffen" : 7, "halles" : 8, "neudorf" : 9, "robertsau" : 10, "gare" : 11, "musau" : 12, "orangerie" : 13, "krutenau" : 14, "forêt noire" : 15, 'centre-ville' : 16, "ostwald" : 17, "illkirch-graffenstaden" : 18, "bischheim" : 19, "lingolsheim" : 20, "schiltigheim" : 21, "port du rhin" : 22, "hautepierre":23, "contades":24, "oberhausbergen" : 25}
    key = list(quartiers.keys())
    quartier = 0
    text = soup.find("div", class_='description text_body_1 mt-2').text
    text = text.lower().split()
    if (get_ville_nexity(soup)==["Strasbourg"])==False:
        for i in range(len(key)):
            if (get_ville_nexity(soup)[0].lower().find(key[i]) != -1)==True:
                quartier = [key[i].capitalize()]
                q_num = [float(quartiers.get(key[i]))]
    else: 
        for i in range(len(key)):
            for j in range(len(text)):
                if (text[j] == key[i])==True:
                    quartier = [key[i].capitalize()]
                    q_num = [float(quartiers.get(key[i]))]
                    break
            if (quartier == 0) == True:
                quartier = ["nan"]
                q_num = [float("nan")]
                
    return quartier + q_num

# c) Caractéristiques spécifiques (Type, Loyer, Charges, Pièces, Surface, Ascenseur, Balcon, Terrain, Terrasse, Parking, 
#                                  Cave, Etage) 
def get_carac_nexity(soup, word):
    text = soup.find_all("div", class_='d-flex align-items-center')
    var = 'R'
    for i in range(len(text)):
        et = text[i].text.lower()
        et1 = et.split()
        if (et.find(word) != -1) == True:
            if (word == 'terrain')==True:
                if (et1[len(et1)-1]=="non")==True:
                    var = float(0)
                else:
                    var = float(1)
                break
            if (word == "parking")==True:
                if (et1[len(et1)-1]=="non")==True:
                    var = float(0)
                else:
                    var = float(1)
                break
            if (word == "etage")==True:
                if (et1[1]=="rdc")==True:
                    var = float(0)
                else:
                    var = float(re.findall(r'\d+', et1[1])[0])
                break
            if (word == "surface")==True:
                var = float(re.findall(r'\d+', et1[1])[0])
            else:
                if (word == "loyer" or word == "charges" or word == "pièce") == True:
                    var = float(et1[len(et1)-1])
                    break
                if (word == "type") == True:
                    var = et1[len(et1)-1]
                else:
                    var = et1[len(et1)-1].capitalize()
                    if (var == "Oui")==True:
                        var = float(1)
                    else:
                        var = float(0)
            break
            break
            break
            break
    if (var=="R")==True:
        var = float("nan")
    return [var]  

# d) Performance énergétique
def get_nrj_nexity(soup):
    text = soup.find_all("div", class_='item-indice--value indice-dpe')
    if (text==[])==True:
        text = soup.find_all("div", class_='item-indice--value indice-dpe--f-or-g')
    if (text==[])==False:
        dpe = [float(text[0].find("span").text)]
        ges = [float(text[1].find("span").text)]
        data = dpe + ges
    else:
        data = [float("nan"), float("nan")]
    return data

# e) Meublé
# Sur chaque annonce meublé, il y a une petite bulle en haut à gauche qui indique 'location meublée'. Donc il faut regardé
# si cela apparait.
def get_meuble_nexity(soup):
    capsule = soup.find_all("div", class_='flap flap--not-new')
    if (capsule == [])==True:
        meuble = float(0)
    else:
        capsule = capsule[0].text
        if (str(capsule)=='location meublée')==True:
            meuble = float(1)
        else:
            meuble = float(0)

    return [meuble]

# Fonction qui nous donne toutes les caractéristiques d'une annonce ORPI à l'aide des fonctions précédentes 
def get_nexity(urlpage):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    soup = get_page(urlpage)
    link = [urlpage]
    appart = get_carac_nexity(soup, "type") + get_ville_nexity(soup) + get_quartier_nexity(soup) +  get_carac_nexity(soup, "loyer")  + get_carac_nexity(soup, "charges") + get_carac_nexity(soup, "pièce") + get_carac_nexity(soup, "surface") + get_meuble_nexity(soup) + get_carac_nexity(soup, "ascenseur") + get_carac_nexity(soup, "balcon") + get_carac_nexity(soup, "terrasse") + get_carac_nexity(soup, "cave") + get_carac_nexity(soup, "parking") + get_carac_nexity(soup, "terrain") + link
    return appart