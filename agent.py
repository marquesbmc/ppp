# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 12:44:14 2023

@author: beLIVE
"""

import random, math
from realm import Realm
from plant import Plant
from operator import itemgetter, attrgetter
from parameters import ZERO, ONE, TWO, MARGIN, breed, random, REALM_WIDTH, REALM_HEIGHT, RAY, VALOR_EAT


class Agent:       
    def __init__(self, realm, age_limit, energy, ray, v_eat):
        self._breed = breed[ONE][ZERO] # prey
        self._food = breed[ZERO][ZERO]# plant
        self._age = ZERO
        self._energy = energy
        self._age_limit = age_limit
        self._is_life = True
        self._coord_x = None
        self._coord_y = None
        self._realm = realm
        self._ray = ray
        self._valor_eat = v_eat
  

        # cria nova prey respeitando espaco vazio e total de tentativas   
        var_logic = True # variavel de controle do enlaco while
        limit = 99 # limite maximo de inserir plant no realm
        count = 0 # total de tentativa para inserir plant no realm 
        x = 0
        y = 0
        
        while var_logic:
            count +=1
            element_candidate = self._realm.get_empty()
                
            if element_candidate != 0:           
                 x = element_candidate[ZERO]
                 y = element_candidate[ONE]
           
            if self._realm.is_add_iten(x, y, int(self._breed)):
                self._coord_x = x
                self._coord_y = y                
                var_logic = False  
                    
            if count >= limit:
                var_logic = False
        
        
    def reproduce(self, dist_reproduce):
        res = False
        list_reproduce = []
        v_dist_reproduce = dist_reproduce
        list_reproduce = self._radar(v_dist_reproduce, ZERO)
        
        if len(list_reproduce) != ZERO:
            new_agent = random.choice(list_reproduce)
            res = self._realm.is_add_iten(new_agent[ZERO], new_agent[ONE], int(self._breed))
        
        return res
        
    def delete(self):
        print(self._coord_x, self._coord_y)
        self._realm.delete_item(self._coord_x, self._coord_y)
        self._energy = 0
        self._is_life = False

    def action(self):
        
        # limite do radar
        # esse relatorio pode ajudar self._realm.rel_total_iten_value()[1][2] > ZERO
         
        fx = 0
        fy = 0
        
        target_dist = 0
        target_x = 0
        target_y = 0
        list_target = self._hunt()
        
        # Se existe pelo menos 1 alvo _E_ o alvo é comida _E_ o agente esta vivo
        if len(list_target) != ZERO and self._realm.is_contains(target_x, target_y) == self._food and self._check_life:
            print("entrou!")
            target_dist = list_target[ZERO]
            target_x = list_target[ONE]
            target_y = list_target[TWO]
            
            #Se o alvo esta com distacia igual 1, somente comer
            if target_dist == ONE:
                print("distancia = 1")
                if not self.eat(target_x, target_y): #nao conseguiu se alimentar
                    print("nao conseguiu se alimentar")
                    self._energy -= ONE
                print("se alimentou")    
                
            #Se o alvo esta com distacia maior 1, criar vetor velocidade
            else:
                print("distancia > 1")
                
                #contrucao do vetor direcao ((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1))
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
            print("nao achou alvo")
            self._ray += 1
            self._energy -= ONE
        
        # ATENCAO RETIRAR IDADE +1 RESPONSABILIDADE DO MAIN
        self._age += 1
        self._check_life()
        
    def eat(self, pos_x, pos_y):
        
    
        print("comeu")
        res1 = self._realm.delete_item(pos_x, pos_y)
        res2 = self._realm.update_local_iten(self._coord_x, self._coord_y, pos_x, pos_y)
        self._coord_x = pos_x
        self._coord_y = pos_y
        #criar novo elemento pode vir daqui
        if res1 and res2:
            print("ganhou energia comendo +",self._valor_eat )
            self._energy += self._valor_eat
        
        return res1 and res2
    
    def _radar_old(self, ray):
        self._list_target = []
        ray_x = 0
        ray_y = 0
        
        if self._coord_x - ray <= MARGIN + ZERO: 
            px = MARGIN
            ray_x = self._coord_x - ray
        else: px = self._coord_x - ray
        
        if self._coord_y - ray <= MARGIN + ZERO: 
            py = MARGIN
            ray_y = self._coord_y - ray
        else: py = self._coord_y - ray
    
        for l in range(2*ray + ray_x +1): #fixa linha
            for c in range(2*ray + ray_y +1): #fixa coluna
                if l+px < self._realm.get_width() + MARGIN and c+py < self._realm.get_height() + MARGIN:
                    #self._realm.get_type_iten(l+px,c+py)
                    if self._realm.get_type_iten(l+px,c+py) == self._food: # é planta
                        self._list_target.append([l+px,c+py])
        
        return self._list_target
        
    def _border(self, x, y):
        x = max(x, MARGIN)
        x = min(x, REALM_WIDTH + MARGIN)
        y = max(y, MARGIN)
        y = min(y, REALM_HEIGHT + MARGIN)
        
        return [x,y]
    
    def _check_life(self):
        if self._energy < ZERO or self._age > self._age_limit:
            self._is_life = False
            self._realm.delete_item(self._coord_x,self._coord_y)
            print("morreu!")  
             
        return self._is_life
  
    def _radar(self, ray, search_for):
        self._list_target = []
        ray_x = 0
        ray_y = 0
        var_search = search_for
        
        if self._coord_x - ray <= MARGIN + ZERO: 
            px = MARGIN
            ray_x = self._coord_x - ray
        else: px = self._coord_x - ray
        
        if self._coord_y - ray <= MARGIN + ZERO: 
            py = MARGIN
            ray_y = self._coord_y - ray
        else: py = self._coord_y - ray
        
        #ray_x = self._border(ray_x, ray_y)[ZERO]
        #ray_y = self._border(ray_x, ray_y)[ONE]
    
        for l in range(2*ray + ray_x +1): #fixa linha
            for c in range(2*ray + ray_y +1): #fixa coluna
                if l+px < self._realm.get_height() + MARGIN and c+py < self._realm.get_width() + MARGIN:
                    if [self._coord_x,self._coord_y] != [l+px, c+py] :
                        if self._realm.get_type_iten(l+px,c+py) == var_search: # procurado por
                            self._list_target.append([l+px,c+py])
        
        return self._list_target
    
    def _hunt(self):
            target = []
            list_dist_target = []
            
            # lista de alvos do radar
            list_target = self._radar(self._ray,self._food )
            
            if len(list_target) != ZERO:
                for t in range(len(list_target)):
                    
                    dist_square = round(math.sqrt((self._list_target[t][ZERO] - self._coord_x )**TWO + (self._list_target[t][ONE] - self._coord_y)**TWO))
                    list_dist_target.append([dist_square,self._list_target[t][ZERO],self._list_target[t][ONE]])
               
                # ordena lista em relacao a distancia
                list_dist_target = sorted(list_dist_target, key=itemgetter(0))
                
            
                # Alvo = distacia, coordx , coord y
                target = list_dist_target[ZERO]
            
            return target


    
class Prey(Agent):
    def __init__(self, realm, age_limit, energy, ray, v_eat):
        super().__init__(realm, age_limit , energy, ray, v_eat)
        
        self.age_limit = age_limit
        

class Predator(Agent):
    def __init__(self, realm, age_limit, energy, ray, v_eat):
        super().__init__(realm, age_limit , energy, ray, v_eat)
        
        self.age_limit = age_limit

