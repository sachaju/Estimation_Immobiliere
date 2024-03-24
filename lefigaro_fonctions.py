# a) avoir le type du bien
def get_type_lf(soup):
    text = soup.find_all('h1')[0].text.lower()
    if 'appartement' in text or 'studio' in text or 'location' in text:
        typ='Appartement'
    elif 'Maison' in text:
        typ='Maison'
    return [typ]

# b) Récupération de la ville : Strasbourg et alentour
def get_ville_lf(soup):
    text = soup.find_all('h1')[0].text
    ville = re.search(r'à (\w+)', text).group(1)
    return[ville]

# c) Le nombre de pièces et la surface
def get_piece_lf(soup):
    text= soup.find_all('span', class_='feature')
    for i in range(len(text)):
        et = text[i].text.split()
        if "surface" in et:
            surface = float(re.match(r'([\d.]+)', et[0]).group())
        if "pièces" in et or 'pièce' in et:
            pièces = float(re.match(r'([\d.]+)', et[0]).group())
    return [pièces, surface]

# d) Loyer et Charges
def get_loyer_charges_lf(soup):
    loyer = soup.find_all('span', class_='price')[0].text
    loyer = float(re.sub(r'[^\d.]', '', loyer))
    charges = soup.find_all('span', class_='about-price-fees-label')
    if (charges == [])==True:
        charges = 0
    else:
        charges = charges[0].text
        charges = float(re.search(r'\d+', charges).group())
    if "CC" in (soup.find_all('span', class_='price')[0].text):
        loyer = loyer - charges
    return [loyer, charges]

# e) Caractéristique : Ascenseur, Balcon, Terrasse, cave, jardin, parking
def get_carac_lf(soup, word):
    Var = ["ascenseur", "balcon", "terrasse", "cave", "jardin", "parking"]
    text = soup.find_all("li", class_='options')
    carac = float(0)
    if (text == [])==True:
        carac = float(0)
    else :
        for i in range(len(text)):
            for j in range(len(Var)):
                if (word == text[i].text.lower())==True:
                    carac = float(1)
    return [carac]

# f) Meuble
def get_meuble_lf(soup):
    text = soup.find_all("p", class_='truncated-description')[0].text.lower()
    if "meublé" in text:
        meuble = float(1)
    else:
        meuble = float(0)
    return [meuble]

# g) Quartier
def get_quartier_lf(soup):
    quartiers = {"meinau" : 1, "neustadt" : 2, 'poteries' : 3, "esplanade" : 4, "petite france" : 5, "cronenbourg" : 6, "koenigshoffen" : 7, "halles" : 8, "neudorf" : 9, "robertsau" : 10, "gare" : 11, "musau" : 12, "orangerie" : 13, "krutenau" : 14, "forêt noire" : 15, 'centre-ville' : 16, "ostwald" : 17, "illkirch-graffenstaden" : 18, "bischheim" : 19, "lingolsheim" : 20, "schiltigheim" : 21, "port du rhin" : 22, "hautepierre":23, "contades":24, "oberhausbergen" : 25}
    key = list(quartiers.keys())
    text = soup.find_all("p", class_='truncated-description')
    text = text[0].text.lower()
    quartier = 0

    if (get_ville_lf(soup)==["Strasbourg"])==False:
        for i in range(len(key)):
            if (get_ville_lf(soup)[0].lower().find(key[i]) != -1)==True:
                quartier = [key[i].capitalize()]
                q_num = [float(quartiers.get(key[i]))]
    else:    
        for i in range(len(key)):
            if (text.find(key[i]) != -1)==True:
                quartier = [key[i].capitalize()]
                q_num = [float(quartiers.get(key[i]))]

    if (quartier == 0) == True:
        quartier = ["nan"]
        q_num = [float("nan")]
        
    return quartier + q_num

# h) honoraires
def get_honoraires_lf(soup):
    text = soup.find_all('li', class_='item-about-price')
    honoraires = [float('nan')]
    for i in range(len(text)):
        if "honoraires" in text[i].text.lower():
            if "non communiqué" in text[i].text.lower():
                honoraires = [float('nan')]
            else:
                honoraires = [float(re.search(r'\b\d+\b',text[2].text.lower())[0])]
    return honoraires

def get_lefigaro(urlpage):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    soup = get_page(urlpage)
    link = [urlpage]
    appart = get_type_lf(soup) + get_ville_lf(soup) + get_quartier_lf(soup) + get_loyer_charges_lf(soup) + get_honoraires_lf(soup) + get_piece_lf(soup) + get_meuble_lf(soup) + get_carac_lf(soup, "ascenseur") + get_carac_lf(soup, "balcon") + get_carac_lf(soup, "terrasse") + get_carac_lf(soup, "cave") + get_carac_lf(soup, "parking") + get_carac_lf(soup, "jardin") + link
    return appart