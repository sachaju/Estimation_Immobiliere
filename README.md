# Estimation immobilière

## Description du projet :  

Objectifs :  
- Estimer le prix d'un bien immobilier selon ses caractéristiques et l'offre actuelle du marché strasbourgeois  
- Proposer une liste d'annonces disponibles sur internet selon des caractéristiques souhaitées dans les environs de Strasbourg  
- Créer une base de données de l'offre actuelle du marché immobilier strasbourgeois  

## Description des fichiers :
1) `Basics_estimations_fonctions.py` : Regroupement de fonctions utilisées pour faire du scraping et traiter les données des sites immobiliers : Obtenir le HTML, obtenir les liens des annonces, importer les données,...
2) `orpi_fonctions.py` : Regroupement des fonctions pour obtenir les différentes caractéristiques des logements des annonces du site Orpi
3) `nexity_fonctions.py` : Regroupement des fonctions pour obtenir les différentes caractéristiques des logements des annonces du site Nexity
4) `lefigaro_fonctions.py` : Regroupement des fonctions pour obtenir les différentes caractéristiques des logements des annonces du site Lefigaro immobilier
5) `estimation_immobilier_fonctions.py` : Regroupement des fonctions `estimation()` et `annonces()`

## Libraries nécessaires :  
- pandas  
- numpy  
- bs4
- scikit-learn
- scipy 

## Guide d'utilisation :  

1) Estimer le prix d'un bien immobilier selon ses caractéristiques

```
import estimation_immobilier_fonctions as immobilier
immobilier.estimation()
```

2) Obtenir une liste d'annonces disponibles sur internet

```
import estimation_immobilier_fonctions as immobilier
immobilier.annonces()
```

 
