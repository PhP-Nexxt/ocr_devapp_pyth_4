#Ocr_Projet4 

#from typing_extensions import Self
#from turtle import color
#from cmath import rect


from ast import Pass
import py_compile


class Rectangle:
    #Variable (Etat) : Initialisation des variables de la classe Rectangle, soit longueur, largeurs et couleurs
    def __init__(self, lenght, withd, color="red"):#couleur par defaut de Rectangle = Rouge
        self.lenght = lenght
        self.withd = withd
        self.color = color
    # Methode (comportement): Calcul de la surface 
    def calculate_area(self):
        return self.lenght * self.withd

class Cercle:
    #Variable (Etat) : Initialisation des variables de la classe Cercle, soit ldiametre et couleurs
    def __init__(self, radius, color="green"):#couleur par defaut de Cercle = Vert
       self.radius = radius
       self.color = color
    # Methode (comportement): Calcul de la surface 
    def calculate_area(self):
        return self.radius * self.radius * 3,14
    # Methode (comportement): Calcul de la circonference
    def calculate_perimeter(self):
        return self.radius * 3
    
#Test instanciation de la classe Rectangle
rect1 = Rectangle(lenght=6, withd=3, color="blue")
rect2 = Rectangle(lenght=23, withd=13, color="Yellow")
area_rect1 = rect1.calculate_area()
area_rect2 = rect2.calculate_area()
print(rect1.color, rect2.lenght)
print("Surface rectangle 1 :", area_rect1)
print("Surface rectangle 2 :", area_rect2)

#Test instanciation de la classe Cercle
cercle1 = Cercle(radius=12, color="pink")
cercle2 = Cercle(radius=8,)
area_cercle1 = cercle1.calculate_area
area_cercle2 = cercle2.calculate_area

perimeter_cercle1 = cercle1.calculate_perimeter
perimeter_cercle2 = cercle2.calculate_perimeter

print(cercle1.radius, cercle2.color)
print("Perimetre cercle 1 :", perimeter_cercle1)
print("Perimetre cercle 2 :", perimeter_cercle2)

print(area_cercle1)
print(area_cercle2)


