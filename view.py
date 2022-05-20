#Ici sont gerer tous les affichages



#Import des paquets Python nécessaires à l'execution du programme
from tinydb import TinyDB, Query


db_joueurs = TinyDB("/Users/philippepras/Documents/ocr_devapp_pyth_4/db_joueurs.json")



#liste_joueurs = 

print(db_joueurs.all())

#print(liste_joueurs)

#Query() # base "Joueurs"