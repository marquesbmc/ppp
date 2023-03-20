# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 19:37:08 2023

@author: beLIVE
"""
import random
from parameters import ZERO, ONE, MARGIN, breed, random
from realm import Realm

class Plant():
    def __init__(self, Realm, age_limit = 10):
        self._breed = breed[ZERO][ZERO] # plant
        self._age = ZERO
        self._age_limit = age_limit
        self._is_life = True
        self._coord_x = None
        self._coord_y = None
        self._realm = Realm                                                                 

        #Cria plant
        # cria nova plant respeitando espaco vazio e total de tentativas   
        var_logic = True # variavel de controle do enlaco while
        limit = 99 # limite maximo de inserir plant no realm
        count = 0 # total de tentativa para inserir plant no realm 
        
        while var_logic:
            count +=1
            x = random.randint(ZERO + MARGIN, self._realm.get_width() - (MARGIN + ONE) )
            y = random.randint(ZERO + MARGIN, self._realm.get_height() - (MARGIN + ONE) )
            
            
            if self._realm.is_add_iten(x, y, int(self._breed)):
                self._coord_x = x
                self._coord_y = y                
                var_logic = False

                
            if count >= limit:
                var_logic = False

        
        print(self._coord_x,self._coord_y)
    
    #Atualiza plant no ciclo
    def update(self):
        self._age += ONE
        if self._is_life == True:
            if self._age >= self._age_limit:
                self.delete()
    
    #Deleta plant
    def delete(self):
        self._realm.delete_item(self._coord_x, self._coord_y)
        self._energy = 0
        self._is_life = False