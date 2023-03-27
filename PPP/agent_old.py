# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 12:44:14 2023

@author: beLIVE
"""
import time
import random, math
from realm import Realm
from plant import Plant
from operator import itemgetter, attrgetter
from parameters import ZERO, ONE, TWO, MARGIN, BREED, random, REALM_WIDTH, REALM_HEIGHT, RAY, VALOR_EAT


class Agent:       
    def __init__(self, realm, energy, ray, age_limit, breed, food, valor_food, child):
        self._breed = breed
        self._food = food
        self._energy = energy
        self._age = ZERO
        self._age_limit = age_limit
        self._is_alive = True
        self._coord_x = None
        self._coord_x = None
        self._realm = realm
        self._ray = ray
        self._child = child

        #Cria plant
        # cria nova plant respeitando espaco vazio e total de tentativas   
        var_logic = True # variavel de controle do enlaco while
        count = 0 # total de tentativa para inserir plant no realm 
        x = 0
        y = 0
        element_candidate = None
        ini = time.time()
        
        #verifica se a variavel child contem elemento se tive cria novo agentecom as coord indicadas
        
        
        if self._child != [] and self._child != None:
            #print("child: ",child)
            x = self._child[ZERO]
            y = self._child[ONE]
            
            if self._realm.is_add_iten(x, y, int(self._breed)):
                    self._coord_x = x
                    self._coord_y = y
                    #print("coordx, coordy: ", self._coord_x, self._coord_y)
        elif self._child == None:
            self._is_alive = False
        else:
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
        
        fim = time.time()
        #print ("Tempo de criacao: ", fim-ini)
    
    # Retorna as coordenada x, y
    def get_coord(self):
        return [self._coord_x, self._coord_y]
    
    
        
    def delete(self,pos_x, pos_y):
        assert type(pos_x) != type(None) , "Update: pos_x == None"
        assert pos_x >= MARGIN , "pos_x abaixo do realm"
        assert pos_x <= REALM_HEIGHT - ONE - MARGIN , "pos_x acima do realm"
            
        assert type(pos_y) != type(None), "Update: pos_y == None"
        assert pos_y >= MARGIN, "pos_y abaixo do realm" 
        assert pos_y <= REALM_WIDTH - ONE - MARGIN, "pos_y fora a direita do realm"
        
        
        return self._realm.delete_item(pos_x, pos_y)

    def update(self):
        
        assert type(self._coord_x) != type(None) , "Update: pos_x == None"
        assert self._coord_x >= MARGIN , "pos_x abaixo do realm"
        assert self._coord_x <= REALM_HEIGHT - ONE - MARGIN , "pos_x acima do realm"
            
        assert type(self._coord_y) != type(None), "Update: pos_y == None"
        assert self._coord_y >= MARGIN, "pos_y abaixo do realm" 
        assert self._coord_y <= REALM_WIDTH - ONE - MARGIN, "pos_y fora a direita do realm"
        
        # limite do radar
        # esse relatorio pode ajudar self._realm.rel_total_iten_value()[1][2] > ZERO
         
        fx = 0
        fy = 0
        
        list_target = []
        target_dist = None
        target_x = None
        target_y = None
        
        #print( "In Update -> self._coord_x, self._coord_y", self._coord_x, self._coord_y )
        #print( "In Update -> hunt", self._hunt() )
        list_target = self._hunt()
        
        if len(list_target) != ZERO:
            #print("Entra 1")
            
            target_dist = list_target[ZERO]
            target_x = list_target[ONE]
            target_y = list_target[TWO]
        
            # Se existe pelo menos 1 alvo _E_ o alvo esta vivo
            if self.is_alive() == "_TRUE_" and self._realm.get_type_iten(target_x, target_y) == self._food:
    
                #print("entrou!.... alvo existe")
                    
                #Se o alvo esta com distacia igual 1, somente comer
                if target_dist == ONE:
                    #print("In update -> eat x, y",target_x, target_y )
                    self.eat(target_x, target_y) 
                        
                #Se o alvo esta com distacia maior 1, criar vetor velocidade
                else:
                    #print("distancia > 1")
                        
                    #contrucao do vetor direcao 
                    if target_x - self._coord_x > ZERO: fx = 1 
                    else: fx = -1
                    if target_y - self._coord_y > ZERO: fy = 1 
                    else: fy = -1
                        
                    #construcao vetor deslocamento dx, dy
                    dx = self._coord_x + fx
                    dy = self._coord_y + fy
                        
                    #colocar na borda
                    dx = int(self._border(dx,dy)[ZERO])
                    dy = int(self._border(dx,dy)[ONE])
                        
                        
                    # Se a movimentacao obteve sucesso
                    if self._realm.update_local_iten(self._coord_x, self._coord_y, dx, dy):
                        self._coord_x = dx
                        self._coord_y = dy
                        self._energy -= ONE
                               
            # Se nao existir alvo
            else:
                #print("nao achou alvo")
                self._ray += 1
                self._energy -= ONE
                
        
        # ATENCAO RETIRAR IDADE +1 RESPONSABILIDADE DO MAIN
        self._age += ONE
        #self._check_life()
        
    def eat(self, pos_x, pos_y):
        assert type(self._coord_x) != type(None) , "pos_x == None"
        assert self._coord_x >= MARGIN , "pos_x abaixo do realm"
        assert self._coord_x <= REALM_HEIGHT - ONE - MARGIN , "pos_x acima do realm"
        
        assert type(self._coord_y) != type(None), "pos_y == None"
        assert self._coord_y >= MARGIN, "pos_y fora a esquerda do realm"
        assert self._coord_y <= REALM_WIDTH - ONE - MARGIN, "pos_y fora a direita do realm"
        
        
        #print("In eat ,self._coord_x, self._coord_y, pos_x, pos_y", self._coord_x, self._coord_y, pos_x, pos_y )
        
        
        res1 = self.delete(pos_x, pos_y)
        res2 = self._realm.update_local_iten(self._coord_x, self._coord_y, pos_x, pos_y)
        
        #print("Comeu",self._coord_x, self._coord_y, pos_x, pos_y )
        self._coord_x = pos_x
        self._coord_y = pos_y
        #criar novo elemento pode vir daqui
        if res1 and res2:
            #print("ganhou energia comendo +",self._valor_eat )
            self._energy += VALOR_EAT

   
    
    def is_alive(self):
        
        #assert type(self._coord_x) != type(None) , "pos_x == None"
        #assert self._coord_x >= MARGIN , "pos_x abaixo do realm"
        #assert self._coord_x <= REALM_HEIGHT - ONE - MARGIN , "pos_x acima do realm"
            
        #assert type(self._coord_y) != type(None), "pos_y == None"
        #assert self._coord_y >= MARGIN, "pos_y abaixo do realm" 
        #assert self._coord_y <= REALM_WIDTH - ONE - MARGIN, "pos_y fora a direita do realm"
        
        resp = "_TRUE_"
        
        #print("Entrou em is_alive")
        if type(self._coord_x) == type(None) or  type(self._coord_y) == type(None):
            print("Entrou em is_alive = None")
            self.is_alive = False
            self._energy = - ONE
            self._age = self._age_limit
            resp = "_FALSE_"
        else:
            if self._coord_x > REALM_HEIGHT - ONE - MARGIN or self._coord_y > REALM_WIDTH - ONE - MARGIN:
                print("Entrou em is_alive > REALM_HEIGHT - ONE - MARGIN")
                self.is_alive = False
                self._energy = - ONE
                self._age = self._age_limit
                resp = "_FALSE_"
            
            if self._coord_x < MARGIN or self._coord_y < MARGIN:
                #print("Entrou em is_alive <  MARGIN")
                self.is_alive = False
                self.energy = - ONE
                self._age = self._age_limit
                resp = "_FALSE_"
            
            if self._age >= self._age_limit + ONE:
                #print("Entrou em is_alive >= self._age_limit + ONE")
                self.is_alive = False
                self._energy = - ONE
                resp = "_FALSE_"
                
            if self._energy < ZERO:
                #print("Entrou em is_alive: self._energy < ZERO")
                self.is_alive = False
                self._age = self._age_limit
                resp = "_FALSE_"
    
            if self.is_alive == False:
                #print("Entrou em is_alive: self.is_alive == False:")
                self._energy = - ONE
                self._age = self._age_limit
                resp = "_FALSE_"
                
            if self.is_alive is False:
                #print("Entrou em is_alive: self.is_alive is False:")
                resp = "_FALSE_"
                self.delete(self._coord_x, self._coord_y)
                
                
        #print("Entrou em is_alive: resp:", resp)
        return resp   
    
    def _border(self, x, y):
        x = max(x, MARGIN)
        x = min(x, REALM_WIDTH - ONE + MARGIN)
        y = max(y, MARGIN)
        y = min(y, REALM_HEIGHT - ONE + MARGIN)
        
        return [x,y]
    
    def _check_life(self):
        if self._energy < ZERO or self._age > self._age_limit:
            self._realm.delete_item(self._coord_x,self._coord_y)
            self.delete()
        return self._is_alive
     
   
    
    
    def _hunt(self):
            target = None
            list_dist_target = []
            
            
############################################################################################            
            # Captura lista de alvos do radar
            list_target = self._radar(self._ray, self._food )
           
############################################################################################            
            # Caso exista elemento list_target retornar o de menor distancia
            if len(list_target) != ZERO:
                for t in range(len(list_target)):
                    
                    dist_square = round(math.sqrt((self._list_target[t][ZERO] - self._coord_x )**TWO + (self._list_target[t][ONE] - self._coord_y)**TWO))
                    list_dist_target.append([dist_square,self._list_target[t][ZERO],self._list_target[t][ONE]])

############################################################################################ 
                # ordena lista em relacao a distancia
                list_dist_target = sorted(list_dist_target, key=itemgetter(0))
                
############################################################################################ 
                # Alvo = distacia, coordx , coord y
                
                target = list_dist_target[ZERO]
                
                
############################################################################################
        
            if target == None:
                target = []
            
            #print("In hunt -> target: ",target)
            return target

 
class Prey(Agent):
    def __init__(self, realm, energy = 10, ray = 1, age_limit = 1000, breed = 2, food = 1, valor_food = 30, child = []):
        super().__init__(realm,  energy, ray, age_limit,  breed, food, valor_food, child)
        #self.age_limit = age_limit
        

class Predator(Agent):
    def __init__(self, realm, energy = 10, ray = 1, age_limit = 100, breed = 3, food = 2, valor_food = 10, child = []):
        super().__init__(realm,  energy, ray, age_limit,  breed, food, valor_food, child)
        #self.age_limit = age_limit

    