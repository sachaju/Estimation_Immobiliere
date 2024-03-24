# Fonction pour avoir la le code html pour une page internet quelconque
def get_page(urlpage):
    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}
    # Timer qui retard l'envoi de requête vers le site pour pas se faire ban
    time.sleep(0.2 + np.random.rand()/10)
    res = requests.get(urlpage, headers = user_agent)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# On obtient le nombre de page d'annonce du site lefigaro car il y a plusieurs page
def get_nb_pagelink(urlpage):
    website = "https://immobilier.lefigaro.fr"
    l = []
    nl = [urlpage]
    while l != "VIDE":
        soup = get_page(urlpage) 
        lnp = soup.find_all("a", "router-link-active router-link-exact-active btn-pagination")
        for i in range(len(lnp)):
            if lnp[i].text == "Suivant":
                l = re.findall('href="(.*?)" ', str(lnp[i]))[0]
                urlpage = website + l
                nl.append(urlpage)
                break
            else:
                l = "VIDE"
    return nl

# Obtenir les liens des annonces pour les sites orpi, nexity et lefigaro
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
    
    # On charge la page d'acceuil ou toutes les annonces sont énumérées
    soup = get_page(urlpage) 
    # On recupère les infos dans le html
    annonces = soup.find_all(a, class_= b)
    # On initialise un vecteur vide pour stocker les liens des annonces
    links = []
    
    for i in range(len(annonces)):
        text = str(annonces[i]) #On met chaque annonce en chaine de caractère
        link = re.findall(reg, text)[0] # On cherche la regular expression qu'on a définit plsu haut
        path = website + link # On regroupe le nom du site et le nom de l'annonce
        links.append(path) # On l'ajoute à notre vecteur "links"
        
    return links

# Fonction finale qui renvoit les caractéristiques d'une annonce d'un site spécifiques !
def get_appart(site):
    links = get_link(site)
    var = ["Type", "Ville", "Quartier", "Quartier_num", "Loyer", "Charges", "Pièces", "Surface", "Meublé", "Ascenseur", "Balcon", "Terrasse", "Cave", "Parking", "Terrain", "Liens"]
    data = []
    if (site=="orpi")==True:
        for i in range(len(links)):
            info = get_orpi(links[i])
            data.append(info)
    if (site=="nexity")==True:
        for i in range(len(links)):
            if (links[i].find("residence_etudiant") != -1)==False:
                info = get_nexity(links[i])
                data.append(info)
    data = pd.DataFrame(data, columns=var)
    return data  

# Fonctions d'importation des données des logements et trie des valeurs manquantes et des doublons
def import_data(site):
    t = time.time()
    if site != "all":
        dt = get_appart(site)
    else:
        dt = pd.concat([get_appart("orpi"), get_appart("nexity"), get_appart("lefigaro")], ignore_index=True)
    dt = dt.dropna(subset=["Loyer", "Surface", 'Charges', 'Pièces', 'Terrain', 'Meublé', 'Ascenseur', 'Balcon', 'Terrasse','Cave','Parking'])
    n=len(dt)-1
    val_double = []
    var = ["Type", "Ville", "Quartier", "Quartier_num", "Loyer", "Charges", "Pièces", "Surface", "Meublé", "Ascenseur", "Balcon", "Terrasse", "Cave", "Parking", "Terrain", "Liens"]
    for i in range(0,n):
        for j in range(i+1,n+1):
            if (dt.iloc[i, 1:-8].tolist() == dt.iloc[j, 1:-8].tolist())==True:
                val_double.append(i)

    dt = dt.drop(list(np.unique(val_double)))
    dt = dt.reset_index(drop=True)
    print((time.time() - t)/60)
    return dt