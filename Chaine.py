from collections import Counter
import unicodedata
import csv

def retirer_caracteres(texte):
    texte = ''.join(c for c in unicodedata.normalize('NFD', texte) if (unicodedata.category(c) != 'Mn' and c != '-'))
    return texte

def compteur_mots(Liste_de_mots_SEO):
    with open(Liste_de_mots_SEO, 'r', encoding='utf-8') as fichier:

        texte_SEO = retirer_caracteres(fichier.read())

    Mots_SEO = texte_SEO.split()


    fichier.close()

    return Mots_SEO



def suppression_parasites(Mots_SEO, fichier_csv):
    with open(fichier_csv, 'r', encoding='utf-8') as fichier:
        lecteur_csv = csv.reader(fichier)
        mots_parasites = [ligne[0] for ligne in lecteur_csv]


    fichier.close()

    print(mots_parasites)
    mots_SEO_propres = [mot for mot in Mots_SEO if mot not in mots_parasites]
    return mots_SEO_propres


def occurrences (Mots_SEO):
    occurrences = Counter(Mots_SEO)

    liste_occurrences = [{"mot": mot, "occurrence": occurrences[mot]} for mot in occurrences]


    liste_occurrences = sorted(liste_occurrences, key=lambda x: x["occurrence"], reverse=True)

    return liste_occurrences




Liste_de_mots_SEO = "SEO.txt"
Liste_de_mots_parasites = "parasites.csv"

Liste_Mots = compteur_mots(Liste_de_mots_SEO)
mots_SEO_propre = suppression_parasites(Liste_Mots, Liste_de_mots_parasites)
resultat = occurrences(mots_SEO_propre)
print(resultat)