#OCR PROJET 4


#TEST CREATION DE CLASSES & CREATION D'ATTRIBUTS ET DE METHODES D'INSTANCES

#Création de la classe Rectangle
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
    # Methode (comportement): Calcul de la circonference > Methode d'instance(self)
    def calculate_perimeter(self):
        return self.radius * 3.14
    
#Test création de l'instance de la classe Rectangle (instanciation)
rect1 = Rectangle(lenght=6, withd=3, color="blue")
rect2 = Rectangle(lenght=23, withd=13, color="Yellow")
area_rect1 = rect1.calculate_area()
area_rect2 = rect2.calculate_area()

#Impression des élements de l'instance de la classe Rectangle
print()
print( "Longueur rectangle 1 :",rect1.lenght, "/ Largeur rectangle 1 :", rect1.withd, "/ Couleur rectangle 1 : ", rect1.color)
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
        self.positions = 1, 2
        self.names = name
        
        self.positions[self.positions] = self.name

        @classmethod
        def find_bird(cls, positions):
            if positions in cls.positions:
                return f"On a trouvé un {cls.positions[position]} !"
            
            return "On à rien trouvé..."


Bird.names
Bird.positions
print(Bird.find_bird((2, 5)))


bird = Bird("mouette")

print(Bird.find_bird((1, 2)))

#>>>>>>>>>>>>>>>>>>Lien OCR https://openclassrooms.com/fr/courses/7150616-apprenez-la-programmation-orientee-objet-avec-python/7195794-creez-et-utilisez-des-objets-python