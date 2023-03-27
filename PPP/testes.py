# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:04:18 2023

@author: beLIVE
"""


class Veiculo:
    def __init__(self, tipo, chassi, marca, modelo, ano):
        self.tipo = tipo
        self.chassi = chassi
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        
        
        
class Motocicleta(Veiculo): 
    def __init__(self, tipo, chassi, marca, modelo, ano, cilindrada):
        super().__init__(tipo, chassi, marca, modelo, ano) 
        self.cilindrada = cilindrada
        
        
        
        
class M:
    def ping(self):
        print("ping")

class A:
    def __init__(self, m, id):
        self.id = id
        self.m = m


class B(A):
    def __init__(self,m, id, pong):
        super().__init__(m, id)
        self.pong = pong
        
        
        


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sup(self):
        # Change the "print" to "return" because the print is on caller side.
        return f"{self.name} {self.age} "

        

# The "Subclass" is inherited from "Person"
class Subclass(Person):
    def __init__(self, name, age, language):
        # Call the __init__ method of parent class with the proper parameters
        super().__init__(name, age)
        # Set the "language" as instance variable.
        self.language = language     
