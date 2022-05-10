#OCR PROJET 4 - MODELS

""" Ici sont implementés tous les models (données) nécessaires à la gestion
des tournois. 
Nous allons créer et utiliser ici une classe "Tournois" 
& une classe"Joueurs"   
"""

#Import des paquets Python nécessaires à l'execution du programme
from tinydb import TinyDB, Query

#Documentation tinydb :
#Lien pypi : https://pypi.org/project/tinydb/
#Lien tinydb : https://tinydb.readthedocs.io/en/latest/



#CREATION DES CLASSES & CREATION D'ATTRIBUTS ET DE METHODES D'INSTANCES


#__________________Création de la classe Tournois_________________________
""" Cette classe permet de creer un tournois contenant les informations 
indiquées dans les Spec Techniques. Les variables à initialiser sont : "
- Nom
- Lieu
- Date de début & date de fin
- Nombre de tours (Réglez la valeur par défaut sur 4)
- Tournées avec La liste des instances rondes
- Joueurs avec la liste des indices correspondants aux instances du 
joueur stockées en mémoire
- Contrôle du temps : Bullet, blitz de 1  ou coup rapide, soit 
de 1 min à 60min pour chaque coup
- Description, soit les remarques générales du directeur du tournoi
"""

class Tournois:
    #Variable (Etat) : Initialisation des variables de la classe Tournois
    def __init__(self, nom_tournois: str = "", lieu_tournois: str = "", 
                 date_debut: str = "", date_fin: str = "",
                 nombre_de_tours: int = 4,
                 tournees = [], joueurs = [], 
                 controle_temps_tournois: str = 60,
                 description_tournois: str = ""):
        
        
        self.nom_tournois = nom_tournois
        if self.nom_tournois == "":
            self.DemanderNomTournois()

        self.lieu_tournois = lieu_tournois
        if self.lieu_tournois == "":
            self.DemanderLieuTournois()
        
        self.date_debut = date_debut
        if self.date_debut == "":
            self.DemanderDateDebut()
        
        self.date_fin = date_fin
        if self.date_fin == "":
            self.DemanderDateFin()
        
        self.nombre_de_tours = nombre_de_tours
        if self.nombre_de_tours == "":
            self.DemanderNombreTours()
        
        self.tournees = tournees
        
        
        self.joueurs = joueurs
       
        
        self.controle_temps_tournois = controle_temps_tournois
        if self.controle_temps_tournois == "":
            self.DemanderTempsTournois()
        
        self.description_tournois = description_tournois
        if self.description_tournois == "":
            self.DemanderDescriptionTournois()
        
        print()
        print(f">>> Constructeur de tournois", '>>>', nom_tournois, lieu_tournois,
              date_debut, date_fin, nombre_de_tours, tournees, joueurs, 
              controle_temps_tournois, description_tournois, '<<<')
        print()           
        
    # Methode (comportement): 

    def DemanderNomTournois(self):
        while self.nom_tournois == "":
            self.nom_tournois = input("Entrez le nom du Tournois ? ")
        print()

    def DemanderLieuTournois(self):
            while self.lieu_tournois == "":
                self.lieu_tournois = input("Entrez le lieu du Tournois ? ")
            print()
        
    def DemanderDateDebut(self):
        while self.date_debut == "":
                self.date_debut =\
                    input("Entrez la date de début du Tournois ? ")
        print()

    def DemanderDateFin(self):
        while self.date_fin == "":
                self.date_fin = input("Entrez la date de fin du Tournois ? ")
        print()
        
    def DemanderNombreTours(self):
        while self.nombre_de_tours == "":
                self.nombre_de_tours =\
                    input("Entrez le nombre de tours du Tournois ? ")
        print()       
    
    def DemanderTempsTournois(self):
        while self.controle_temps_tournois == "":
                self.controle_temps_tournois = input("Entrez le temps du \
                    Tournois ? ")
        print()    
    
    def DemanderDescriptionTournois(self):
        while self.description_tournois == "":
                self.description_tournois =\
                    input("Entrez la description du Tournois ? ")
        print()      
        
    def AfficherInfosTournois(self):
        print(f"Le tournois s'appel", self.nom_tournois, "il se déroule à", 
            self.lieu_tournois, " il commence le", self.date_debut,
            "il se termine le ", self.date_fin)
        print(f"Il comporte", self.nombre_de_tours, "tours.",
            "Chaque coup à une durée maximum de", 
            self.controle_temps_tournois, "minutes.")
        print(f"Voici les remarques relatives à ce tournois : ", self.description_tournois)
        print()
        

#Instanciation de la classe Tournois

Tournois1 = Tournois("Tournois test", "Lyon", "28/05/2022", "29/05/2022",
                     "6", "json tournée", "json.joueur", "10",
                     "Ce tournois s'annonce bien !!!")
Tournois1.AfficherInfosTournois()

Tournois2 = Tournois()
Tournois2.AfficherInfosTournois()


#_________________Création de la classe "Joueurs"___________________
"""
Cette classe permet de créer de nouveaux joueurs, afin qu'ils 
puissent participer au tournois.
Selon les SpecThecniques fournies, les variables à initialiser sont :
- Nom de famille
- Prénom
- Date de naissance
- Sexe
- Classement > Il s'agit d'un chiffre positif 
"""

class Joueurs:
    #Variable (Etat) : Initialisation des variables de la classe Joueur :
    def __init__(self, nom: str = "", prenom: str = "", 
                 date_de_naissance: str= "", sexe: str = "",
                 classement: int = 0):
        # Attributs d'instance
        self.nom = nom
        if self.nom == "":
            self.DemanderNom()
                
        self.prenom = prenom
        if self.prenom == "":
            self.DemanderPrenom()
            
        self.date_de_naissance = date_de_naissance
        if self.date_de_naissance == "":
            self.DemanderDateDeNaissance()
        
        self.sexe = sexe
        if self.sexe == "":
            self.DemanderSexe()
            
        self.classement = classement
        if classement != 0:
            self.DemanderClassement()
        
        print()
        print(f">>> Constructeur de joueur >>>", 
              nom, prenom, date_de_naissance, sexe, str(classement), "<<<")
        print()
        
        
    # Methodes d'instance   
    def DemanderNom(self):
        while self.nom == "":
            self.nom = input("Entrez le nom du joueur ? ")
        print()
                
    def DemanderPrenom(self):
        while self.prenom == "":
            self.prenom = input("Entrez le prénom du joueur ? ")
        print()
        
    def DemanderDateDeNaissance(self):
        while self.date_de_naissance == "":
            self.date_de_naissance = input("Entrez la date de naissance du \
                                            joueur ? ")
        print()
        
    def DemanderSexe(self):
        while self.sexe == "":
            self.sexe = input("Entrez le sexe du joueur ? ")
        print()
        
    def DemanderClassement(self):
        self.classement = input("Entrez le classement du joueur ? ")
        print()
        
    def AfficherInfoJoueurs(self):
        print(f"Le joueur crée s'appelle ", self.nom, self.prenom,
              "il est né le ", self.date_de_naissance, "il est de Sexe",
              self.sexe, "son classement dans le tournois est :",
              self.classement)
        print() 


#Instanciation de la classe Joueurs

joueurs1 = Joueurs("Pras", "Philippe", "03/04/1967", "M")
joueurs1.AfficherInfoJoueurs()

joueurs2 = Joueurs()
joueurs2.AfficherInfoJoueurs()
        


        
