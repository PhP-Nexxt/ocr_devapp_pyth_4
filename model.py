#OCR PROJET 4 - MODELS

#Ici sont implementés tous les models (données) nécessaires à la gestion
#des tournois. 
#Nous allons créer et utiliser ici une classe "Tournois" 
#& une classe"Joueurs"   

#Import des paquets Python nécessaires à l'execution du programme
from tinydb import TinyDB, Query

#Documentation tinydb :
#Lien pypi : https://pypi.org/project/tinydb/
#Lien tinydb : https://tinydb.readthedocs.io/en/latest/

#CREATION DES CLASSES & CREATION D'ATTRIBUTS ET DE METHODES D'INSTANCES

#__________________Création de la classe Tournois_________________________
#Cette classe permet de creer un tournois contenant les informations 
#indiquées dans les Spec Techniques. Les variables à initialiser sont : "
#- Nom
#- Lieu
#- Date de début & date de fin
#- Nombre de tours (Réglez la valeur par défaut sur 4)
#- Tournées avec La liste des instances rondes *Voir Tinydb
#- Joueurs avec la liste des indices correspondants aux instances du 
#joueur stockées en mémoire *Voir tiny db
#- Contrôle du temps de jeu : Bullet, blitz de 1  ou coup rapide, soit 
#de 1 min à 60min pour chaque coup
#- Description, informations générales du directeur du tournoi


class Tournois:
    #Variable (Etat) : Initialisation des variables de la classe Tournois
    def __init__(self, nom_tournois: str = "",
                 lieu_tournois: str = "", 
                 date_debut_tournois: str = "", date_fin_tounois: str = "",
                 nombre_de_tours: int = 4,
                 tournees = [], joueurs = [], 
                 controle_temps_jeu: str = 60,
                 description_tournois: str = ""):
    
        self.nom_tournois = nom_tournois
        self.lieu_tournois = lieu_tournois
        self.date_debut_tournois = date_debut_tournois
        self.date_fin_tournois = date_fin_tounois
        self.nombre_de_tours = nombre_de_tours
        #self.tournees = []
        #self.joueurs = []
        self.controle_temps_jeu = controle_temps_jeu
        self.description_tournois = description_tournois
        
    # Methode (comportement): 
    
    def AjouterNouveauTournois(self):
        
        db_tournois = TinyDB("db_tournois.json") #Créa/Init base "Tournois"
        db_tournois.truncate() #Suppression des tournois n-1
        
        print()
        self.nom_tournois = input("Entrez le nom du Tournois ? ")
        print()

        self.lieu_tournois = input("Entrez le lieu du Tournois ? ")
        print()

        self.date_debut_tournois =\
                    input("Entrez la date de début du Tournois ? ")
        print()

        self.date_fin_tournois =\
                    input("Entrez la date de fin du Tournois ? ")
        print()
        
        self.nombre_de_tours =\
                    input("Entrez le nombre de tours du Tournois ? ")
        print()       

        self.controle_temps_jeu = input("Entrez le temps de jeu (en Minutes) ? ")
        print()    
    
        self.description_tournois =\
                    input("Entrez la description du Tournois ? ")
        print()      
        
        #Ajout du joueur dans la base "db_tournois.json"
        db_tournois.insert({"tournament_name": self.nom_tournois, 
                            "tournament_place": self.lieu_tournois,
                            "tournament_first_day": 
                                self.date_debut_tournois,
                            "tournament_last_day": self.date_fin_tournois,
                            "number_of_chess_game": self.nombre_de_tours,
                            "time_per_move": self.controle_temps_jeu,
                            "tournament_informations": 
                                self.description_tournois,
                            } )
        print(f"Le Tournois", self.nom_tournois,\
                "a bien été crée")
        print() 

#L'instanciation de la classe se fait au niveau du programme principal


#_________________Création de la classe "Joueurs"___________________

#Cette classe permet de créer de nouveaux joueurs, afin qu'ils 
#puissent participer au tournois.
#Selon les SpecThecniques fournies, les variables à initialiser sont :
#- Nom de famille
#- Prénom
#- Date de naissance
#- Sexe
#- Classement > Il s'agit d'un chiffre positif 


class Joueurs:
    #Variable (Etat) : Initialisation des variables de la classe Joueur :
    def __init__(self, nom: str = "", prenom: str = "", 
                 date_de_naissance: str= "", sexe: str = "",
                 classement: int = 0):
        # Attributs d'instance
        self.nom = nom                   
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.classement = classement
        
    # Methodes d'instance  
    #Saisie de tous les joueurs du tournois(8)
    def AjouterJoueursTournois(self):
        
        db_joueurs = TinyDB("db_joueurs.json") #Créa/Init base "Joueurs"
        db_joueurs.truncate() #Suppression des joueurs n-1
        
        for i in range(0,8): #Boucle saisie des joueurs
            print()
            print(f"Joueurs", str(i+1))
            self.nom = input("Entrez le nom du joueur ? ")
            print() 
            self.prenom = input("Entrez le prénom du joueur ? ")
            print()
            self.date_de_naissance =\
                input("Entrez la date de naissance du joueur ? ")
            print()
            self.sexe = input("Entrez le sexe du joueur ? ")
            print()  
            self.classement = input("Entrez le classement du joueur ? ")
            print()
            
            #Ajout du joueur dans la base "db_joueur.json"
            db_joueurs.insert({"name": self.nom, "surname": self.prenom,
                    "birthday": self.date_de_naissance, "genre": self.sexe,
                    "rank": self.classement })
            print(f"Le joueur", self.prenom, self.nom,\
                "a bien été ajouté à la base des participants du tournois.")
            print() 
            
#L'instanciation de la classe se fait au niveau du programme principal
             
