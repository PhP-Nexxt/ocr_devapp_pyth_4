#OCR PROJET 4 - MODELS

""" Ici sont implementés tous les models (données) nécessaires à la gestion des tournois. 
Nous allons créer et utiliser ici une classe "Tournois" & une classe "Joueurs"   
"""

#CREATION DES CLASSES & CREATION D'ATTRIBUTS ET DE METHODES D'INSTANCES


#Création de la classe Tournois
"""
class CreerTournois:
    #Variable (Etat) : Initialisation des variables de la classe Tournois
    def __init__(self, nom: str, lieu: str, date: str, nombre_de_tours: int = 4, 
                 tournees = [], joueurs = [], controle_du_temps: str, description: str):
        
        
        self.lenght = lenght
        self.withd = withd
        self.color = color
        
        
    # Methode (comportement): Calcul de la surface 
    def calculate_area(self):
        return self.lenght * self.withd
"""


#______________________________Création de la classe "Joueurs"_____________________________________
"""Cette classe permet de créer de nouveaux joueurs, afin qu'ils puissent participer au tournois
Selon les SpecThecniques fournies, les variables à initialiser sont :
- Nom de famille
- Prénom
- Date de naissance
- Sexe
- Classement > Il s'agit d'un chiffre positif
"""
class Joueurs:
    #Variable (Etat) : Initialisation des variables de la classe Joueur, soit 
    def __init__(self, nom: str = "", prenom: str = "", date_de_naissance: str= "", sexe: str = "",
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
        if self.sexe =="":
            self.DemanderSexe()
            
        self.classement = classement
        if classement != 0:
            self.DemanderClassement()
        
        print()
        print(f">>> Constructeur de joueur", nom, prenom, date_de_naissance, sexe, str(classement))
        print()
        
    # Methodes d'instance   
    def DemanderNom(self):
        print()
        if self.nom == "":
            self.nom = input("Entrez le nom du joueur ? ")
        print()
                
    def DemanderPrenom(self):
        if self.prenom == "":
            self.prenom = input("Entrez le prénom du joueur ? ")
        print()
        
    def DemanderDateDeNaissance(self):
        if self.date_de_naissance == "":
            self.date_de_naissance = input("Entrez la date de naissance du joueur ? ")
        print()
    def DemanderSexe(self):
        if self.sexe == "":
            self.sexe = input("Entrez le sexe du joueur ? ")
        print()
    def DemanderClassement(self):
        if self.classement == "":
            self.classement = input("Entrez le classement du joueur ? ")
        print()
        
    def AfficherInfo(self):
        print(f"Le joueur crée s'appelle ", self.nom, self.prenom, "il est né le ", self.date_de_naissance, 
              "il est de Sexe", self.sexe, "son classement dans le tournois est :", self.classement)
        print()
    
#Instanciation de la classe 

joueurs1 = Joueurs("Pras", "Philippe", "03/04/1967", "M")
joueurs1.AfficherInfo()

joueurs2 = Joueurs()
joueurs2.AfficherInfo()

        


        
    # Methode (comportement): Calcul de la surface 
    #Mettre en place les conditions de saisie (pas de vide etc), uniformiser les dates etc
    #def calculate_area(self):
        #return self.lenght * self.withd
    

"""
class Rectangle:
    #Variable (Etat) : Initialisation des variables de la classe Rectangle, soit longueur, largeurs et couleurs
    def __init__(self, lenght, withd, color="red"):#couleur par defaut de Rectangle = Rouge
        #Attributs d'instance
        self.lenght = lenght
        self.withd = withd
        self.color = color
    # Methode (comportement): Calcul de la surface 
    def calculate_area(self):
        return self.lenght * self.withd

#Création de la classe Cercle
class Cercle:
    #Variable (Etat) : Initialisation des variables de la classe Cercle, soit diametre et couleurs
    def __init__(self, radius, color="green"):#couleur par defaut de Cercle = Vert
       self.radius = radius
       self.color = color
    # Methode (comportement): Calcul de la surface > Methode d'instance(self)
    def calculate_area(self):
        return self.radius * self.radius * 3.14
    #Methode(comportement):Calcul circonference > Methode instance(self)

    def calculate_perimeter(self):
        return self.radius * 3.14
    
#Test création de l'instance de la classe Rectangle (instanciation)
rect1 = Rectangle(lenght=6, withd=3, color="blue")
rect2 = Rectangle(lenght=23, withd=13, color="Yellow")
area_rect1 = rect1.calculate_area()
area_rect2 = rect2.calculate_area()

#Impression des élements de l'instance de la classe Rectangle
print()
print( "Longueur rectangle 1 :", rect1.lenght, "/ Largeur rectangle 1 :", rect1.withd, "/ Couleur rectangle 1 : ", rect1.color)
print()
print( "Longueur rectangle 2 :",rect2.lenght, "/ Largeur rectangle 2 :", rect2.withd, "/ Couleur rectangle 2 : ", rect2.color)
print()
print("Surface rectangle 1 :", area_rect1)
print()
print("Surface rectangle 2 :", area_rect2)
print()

#Test création de l'instance de la classe Cercle (instanciation)
cercle1 = Cercle(radius=12, color="pink")
cercle2 = Cercle(radius=8,)
area_cercle1 = cercle1.calculate_area()
area_cercle2 = cercle2.calculate_area()
perimeter_cercle1 = cercle1.calculate_perimeter()
perimeter_cercle2 = cercle2.calculate_perimeter()

#Impression des éléments de l'instance de la classe Cercle
print("diametre Cercle 1 :", cercle1.radius, "/ Couleur cercle 1 :", cercle1.color)
print()
print("diametre Cercle 2 :", cercle2.radius, "/ Couleur cercle 2 :", cercle2.color)
print()
print("Surface cercle 1 :", area_cercle1)
print()
print("Surface cercle 2 :", area_cercle2)
print()
print("Perimetre cercle 1 :", perimeter_cercle1)
print()
print("Perimetre cercle 2 :", perimeter_cercle2)
print()


#TEST CREATION DE CLASSES & CREATION D'ATTRIBUTS ET DE METHODES DE CLASSES

class Bird:
    names = ("Mouette", "Pigeon", "moineau", "hirondelles")
    positions = {}
    
    def __init__(self, name):
        self.positions = position
        self.names = name
        
        self.positions[self.positions] = self.name

        @classmethod
        def find_bird(cls, positions):
            if positions in cls.positions:
                return f"On a trouvé un {cls.positions1} !"
            
            return "On à rien trouvé..."


Bird.names
Bird.positions
print(Bird.find_bird((2, 5)))


bird = Bird("mouette")

print(Bird.find_bird((1, 2)))

#>>>>>>>>>>>>>>>>>>Lien OCR https://openclassrooms.com/fr/courses/7150616-apprenez-la-programmation-orientee-objet-avec-python/7195794-creez-et-utilisez-des-objets-python
"""