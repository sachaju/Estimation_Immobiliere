# Real Estate Estimation

## Project Description:

### Objectives:
- Estimate the price of a property based on its characteristics and the current market offer in Strasbourg.
- Provide a list of available listings from the internet based on desired characteristics in the Strasbourg area.
- Create a database of the current real estate market offerings in Strasbourg.

## File Descriptions:
1) **`Basics_estimations_fonctions.py`**: A collection of functions used for scraping and processing data from real estate websites: fetching HTML, obtaining listing links, importing data, etc.
2) **`orpi_fonctions.py`**: A collection of functions for obtaining various property characteristics from listings on the Orpi website.
3) **`nexity_fonctions.py`**: A collection of functions for obtaining various property characteristics from listings on the Nexity website.
4) **`lefigaro_fonctions.py`**: A collection of functions for obtaining various property characteristics from listings on the Lefigaro real estate website.
5) **`estimation_immobilier_fonctions.py`**: A collection of functions `estimation()` and `annonces()`.

## Required Libraries:
- requests
- pandas  
- numpy  
- bs4
- scikit-learn
- scipy 

## Usage Guide:

1) **Estimate the price of a property based on its characteristics:**

```python
import estimation_immobilier_fonctions as immobilier
immobilier.estimation()


2) Get a list of available listings from the internet:

```
import estimation_immobilier_fonctions as immobilier
immobilier.annonces()
```

 
