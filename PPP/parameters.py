# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:53:45 2023

@author: beLIVE
"""

import random
import math
from operator import itemgetter, attrgetter

ZERO = 0
ONE = 1
TWO = 2
MARGIN = 0
BREED = [[1, "plant"],[2, "prey"],[3, "predator"]] # agentes possiveis 
REALM_WIDTH = 10 # tamanho largura tela
REALM_HEIGHT = 10 # tamanho altura tela
RAY = 1
VALOR_EAT = 5# valor da energia ao comer