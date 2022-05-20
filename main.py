#OCR PROJET 4 => Développez un programme logiciel en Python

from model import *

#Instanciation de la classe tournois du fichier models.py
Tournois1 = Tournois()
Tournois1.AjouterNouveauTournois()

#Instanciation de la classe Joueurs du fichier models.py
liste_des_joueurs = Joueurs()
liste_des_joueurs.AjouterJoueursTournois()