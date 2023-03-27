# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 19:37:08 2023

@author: beLIVE
"""
import random
from parameters import ZERO, ONE, MARGIN, BREED, random
from realm import Realm

class Plant():
    def __init__(self, realm, age_limit = 1000):
        self._breed = BREED[ZERO][ZERO] # plant
        self._age = ZERO
        self._age_limit = age_limit
        self._is_alive = True
        self._coord_x = None
        self._coord_y = None
        self._realm = realm                                                                 

        #Cria plant
        # cria nova plant respeitando espaco vazio e total de tentativas   
        var_logic = True # variavel de controle do enlaco while
        count = 0 # total de tentativa para inserir plant no realm 
        x = 0
        y = 0
        element_candidate = None
        
        while len(self._realm.get_list_empty()) != ZERO and var_logic:
            count +=1
            element_candidate = self._realm.get_empty_random()
                
            if element_candidate != None:
                 x = element_candidate[ZERO]
                 y = element_candidate[ONE]
                 
                 if self._realm.is_add_iten(x, y, int(self._breed)):
                    self._coord_x = x
                    self._coord_y = y                
                    var_logic = False
        
        
           
    
    #Atualiza plant no ciclo
    def update(self):
        self._age += ONE
        #if self._is_alive == True::
        if self.is_alive == "_TRUE_":
            if self._age > self._age_limit:
                #if not self.is_none():
                    self.delete()
    
    #Deleta plant
    def delete(self):
        #print("self._coord_x, self._coord_y",self._coord_x, self._coord_y)
        if (self._coord_x != None and self._coord_y != None):
            self._realm.delete_item(self._coord_x, self._coord_y)
        #self._energy = 0
        self._is_alive = False
        self._age = self._age_limit + ONE
        
        
    def is_alive(self):
        
        resp = "_TRUE_"
        
        if self._coord_x == None or self._coord_y == None:
            self.is_alive = False
        if self._age >= self._age_limit + ONE:
            self.is_alive = False
        #if self._energy <= ZERO:
        #    self.is_alive = False
        
        if self.is_alive == False:
            resp = "_FALSE_"
        
            
        return resp
            
        