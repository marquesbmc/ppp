# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:21:24 2023

@author: beLIVE
"""

import random
# Importação da IA que está no arquivo ai.py
from parameters import ZERO, ONE, TWO, MARGIN, breed

class Realm():
    def __init__(self, width: int, height: int):
            self._width = width
            self._height = height
            self._list_map_iten = [] # lista que mapeaia todos os itens no realm
            self._list_mov = []  # lista do total de movimento dos itens no realm
            self._list_iten = [[0,"empty"]]
            
    # captura largura
    def get_width(self):
        return self._width
    
    # captura altura
    def get_height(self):
       return self._height
   
    # dado posicao da coord -> retorna True quando item = 0 (zero representa vazio)
    def is_empty(self, pos_x: int, pos_y: int):
        assert (self._width - pos_x) > MARGIN , "pos_x fora do realm"
        assert (self._height - pos_y) > MARGIN, "pos_y fora do realm"
        
        var_empty = False
        if self._list_map_iten[pos_x][pos_y] == ZERO:
            var_empty = True
        return var_empty
   
    # retorna posicionamento elemento vazio, caso nao exista retorna 0
    def get_empty(self):
        list_empty = []
        element = ZERO
        
        for e in self._list_map_iten:
            if self.is_empty(e[ZERO],e[ONE]):
                list_empty.append(e)
        
        if len(list_empty) == ZERO:
            element = random.choice(list_empty)
        
        return element
   
    def is_contains(self, pos_x, pos_y):
        res = False
        if ((self._width - pos_x) > MARGIN) and ((self._height - pos_y) > MARGIN):
            res = True
        return res
   
    # cria mapeamento em lista vazia (Lista de zeros) -> retorna lista de zero
    def create(self):
        assert self._width > ZERO, "width maior que zero"
        assert self._height > ZERO, "height maior que zero"
        
        for line in range(self._width):
            temp_list = []
            for col in range(self._height):
               temp_list.append(ZERO)
            self._list_map_iten.append(temp_list)

        return print(self._list_map_iten)
    
   
    
    # dado posicao da coord -> retorna valor
    def get_type_iten(self, pos_x: int, pos_y: int):
        assert (self._width - pos_x) > MARGIN , "pos_x fora do realm"
        assert (self._height - pos_y) > MARGIN, "pos_y fora do realm"
        return self._list_map_iten[pos_x][pos_y]
    
    # adiciona novo item no mapa -> True item add ou False se local estiver != ZERO
    def is_add_iten(self, pos_x: int, pos_y: int, cod_item: int):
        assert (self._width - pos_x) > MARGIN , "pos_x fora do realm"
        assert (self._height - pos_y) > MARGIN, "pos_y fora do realm"
        assert len(breed) + ONE > cod_item, "cod_item não existe na lista de racas"
        
        response = False
        if self.is_empty(pos_x, pos_y):
            self._list_map_iten[pos_x][pos_y] = cod_item
            response = True
        return response
    
    # exclui item no mapa -> item zerado
    def delete_item(self, pos_x:int, pos_y:int ):
        assert (self._width - pos_x) > MARGIN , "pos_x fora do realm"
        assert (self._height - pos_y) > MARGIN, "pos_y fora do realm"
        
        res = False
        
        if not self.is_empty(pos_x, pos_y):
            
            self._list_map_iten[pos_x][pos_y] = ZERO
            
            if self._list_map_iten[pos_x][pos_y] == ZERO:
                res = True
            
        return res # TRUE elemento deletado
    
    # Processo dinamico de atualizacao pra cada agent, pode ser q nao funcione! necessario testar
    # Outra forma é definir uma fila (lista) de atualizacao
    # Atualiza cada movimento de agentes no mapa
    def update_local_iten(self, pos_x:int, pos_y:int, fut_x:int, fut_y:int):
        assert (self._width - pos_x) > MARGIN , "pos_x fora do realm"
        assert (self._height - pos_y) > MARGIN, "pos_y fora do realm"
        assert (self._width - fut_x) > MARGIN , "pos_x fora do realm"
        assert (self._height - fut_y) > MARGIN, "pos_y fora do realm"
        
        breed = self._list_map_iten[pos_x][pos_y]
        res = False
        if self.is_empty(fut_x,fut_y):
            self._list_map_iten[fut_x][fut_y] = self._list_map_iten[pos_x][pos_y]
            self._list_map_iten[pos_x][pos_y] = ZERO
            res = True
            #adiciona movimento de iten na lista de movimento
            self._list_mov.append([breed, pos_x,pos_y,fut_x,fut_y])
            
        return res
    
    # relatório de total de itens no mapa naquele instante
    def rel_total_iten_value(self):
        lin = self._width
        col = self._height
        valor_iten = ZERO #tipo do iten 0,1,2,3,4

        if len(self._list_iten) != (len(breed) + ONE):
            # popular list_iten com agentes existentes
            for b in range(len(breed)):
                self._list_iten.append(breed[b])
            #add 0 ao total de de breed
            for i in range(len(self._list_iten)):
                self._list_iten[i].append(ZERO)
        else:        
            for i in range(len(self._list_iten)):
                self._list_iten[i][TWO] = 0
        
        
        #preenchendo total elementos
        for l in range(lin):
            for c in range(col):
                valor_iten = self._list_map_iten[l][c] # 0,1,2,3
                self._list_iten[valor_iten][TWO] += ONE
                
        return self._list_iten #list_tot_iten
        
    
    # relatório de movimentacao no mapa
    def rel_update_mov(self):
        return self._list_mov
    
    # apaga um pedaço de mapa
    def catastrofe():
        return "BOOM!!!"
    
    # retorna lista cartesiana
    def map_view(self):
        list = self._list_map_iten
        new_list = []
        leng = len(list)
        
        for n in range(leng-1, -1, -1):
          new_list.append(list[n])
        
        return print (*new_list, sep="\n")
    
    
    
    