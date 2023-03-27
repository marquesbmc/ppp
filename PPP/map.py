# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:04:17 2023

@author: beLIVE
"""

# Variavel Global
_MARGIN = 0
_ONE = 1
_ZERO = 0

class Realm():
    def __init__(self, width: int, height: int):
            self._width = width 
            self._height = height 
            self._list_map_iten = [] # lista que mapeaia todos os itens no plano
            self._list_mov = []  # lista do total de movimento dos itens no realm
            self._list_type_agent = [[0,"empty"], [1, "plant"],[2, "prey"],[3, "predator"]]
            
            
            
            
    def get_width(self):
        return self._width
    
    def get_height(self):
       return self._height
   
    
    def is_empty(self, pos_x: int, pos_y: int):
        # dado posicao da coord -> retorna True quando item = 0 (zero representa vazio)
        assert isinstance(pos_x, int) , "type(pos_x) != int"
        assert pos_x >= _MARGIN , "pos_x abaixo do realm"
        assert pos_x <= self._height - _ONE - _MARGIN , "pos_x acima do realm"
        
        assert isinstance(pos_y, int) , "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert pos_y <= self._width - _ONE - _MARGIN, "pos_y fora a direita do realm"
        
        #var_empty = False
        #if self._list_map_iten[pos_x][pos_y] == _ZERO:
            #var_empty = True
            
        return self._list_map_iten[pos_x][pos_y] == _ZERO