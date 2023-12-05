from collections import Counter
import unicodedata
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def delete_speciaux(texte):
    texte = ''.join(c for c in unicodedata.normalize('NFD', texte) if (unicodedata.category(c) != 'Mn' and c != '-'))
    return texte

def extraction_texte(Liste_de_mots_SEO):
    soup = BeautifulSoup(Liste_de_mots_SEO, 'html.parser')
    texte_sans_balises = soup.get_text(separator=' ')

    texte_sans_balises = delete_speciaux(texte_sans_balises)

    return texte_sans_balises.split()


def  extraction_balises_valeurs(Liste_de_mots_SEO, nom_balise, nom_attribut):
    soup = BeautifulSoup(Liste_de_mots_SEO, 'html.parser')

    balises = soup.find_all(nom_balise)

    valeurs = [balise.get(nom_attribut) for balise in balises if balise.get(nom_attribut) is not None]

    balises_sans_alt = [balise for balise in balises if balise.get(nom_attribut) is None]
    nombre_balises_sans_alt = len(balises_sans_alt)
    return valeurs,nombre_balises_sans_alt


def enlever_parasites(Mots_SEO, fichier_csv):
    # Charge les mots parasites à partir du fichier CSV spécifié
    with open(fichier_csv, 'r', encoding='utf-8') as fichier:
        lecteur_csv = csv.reader(fichier)
        mots_parasites = [ligne[0] for ligne in lecteur_csv]


    fichier.close()

    mots_SEO_propres = [mot for mot in Mots_SEO if mot not in mots_parasites]
    return mots_SEO_propres


def occurrences (Mots_SEO):
    occurrences = Counter(Mots_SEO)

    liste_occurrences = [{"Le mot": mot, "occurrence": occurrences[mot]} for mot in occurrences]

    liste_occurrences = sorted(liste_occurrences, key=lambda x: x["occurrence"], reverse=True)

    return liste_occurrences


def extraction_nom_domaine(url):
    parsed_url = urlparse(url)

    nom_domaine = parsed_url.netloc

    return nom_domaine

def extraction_html(url):
    reponse = requests.get(url)

    if reponse.status_code == 200:

        soup = BeautifulSoup(reponse.content, 'html.parser')

        code_html = str(soup)

        return code_html
    else:
        print("La requête a échoué avec le code :", reponse.status_code)
        return None


def href(valeurs_href, nombre_liens_sortant, nombre_liens_entrant):
    for valeur in valeurs_href:
        if isinstance(valeur, str) and "http" in valeur:
            nombre_liens_sortant += 1
        else:
            nombre_liens_entrant += 1

    return nombre_liens_sortant, nombre_liens_entrant


print("Bienvenue sur l'outil d'audit SEO !")
url = input("Quelle page web souhaitez-vous analyser ?")
Liste_de_mots_parasites = input("Indiquez le chemin du fichier CSV contenant les mots parasites :")
nombre_occurrences = int(input("Combien d'occurrences souhaitez-vous faire remonter ? :"))

nom_domaine = extraction_nom_domaine(url)
print("\nNom de domaine :", nom_domaine,"\n")

code_html = extraction_html(url)

Liste_Mots = extraction_texte(code_html)

mots_SEO_propre = enlever_parasites(Liste_Mots,Liste_de_mots_parasites)

resultat = occurrences(mots_SEO_propre)

for i in range(len(resultat)):
    if nombre_occurrences > 0:
        print(resultat[i])
        nombre_occurrences -= 1
print()

valeurs_href,nombre_balises_sans_href = extraction_balises_valeurs(code_html, 'a', 'href')

nombre = href(valeurs_href,0,0)
print("Nombre de liens entrant(s) :",nombre[1],"\nNombre de liens sortant(s) :",nombre[0])

valeurs_alt,nombre_balises_sans_alt = extraction_balises_valeurs(code_html, 'img', 'alt')
print("Nombre de balises img sans attribut alt :", nombre_balises_sans_alt,"\n")



