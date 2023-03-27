# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:04:17 2023

@author: beLIVE
"""

import logging

logging.basicConfig(
    filename="ppp.log",
    filemode="w",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)

# Variavel Global
_MARGIN = 0
_ZERO = 0
_ONE = 1
_TWO = 2
_BREED = [[0, "empty"], [1, "plant"], [2, "prey"], [3, "predator"]]


class Realm:
    def __init__(self, width: int, height: int):
        assert isinstance(width, int), "type(width) != int"
        assert isinstance(height, int), "type(height) != int"
        assert width >= _ZERO - _MARGIN, "width menor que Zero - Margin"
        assert height >= _ZERO - _MARGIN, "height menor que Zero - Margin"

        self._width = width
        self._height = height
        self._list_map_iten = []
        self._list_mov = []
        self._list_type_agent = [b[_ZERO] for b in _BREED]

        # Cria self._list_map_iten
        for lin in range(self._width):
            temp_list = []
            for col in range(self._height):
                temp_list.append(_ZERO)

            self._list_map_iten.append(temp_list)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_type_iten(self, pos_x: int, pos_y: int):
        # logging.info(f'{"[Realm] -> _get_type_iten: inicio ..."}')
        # logging.info(f'{"[Realm] -> _get_type_iten:"}{" "}{pos_x}{" "}{pos_y}')
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert pos_y <= self._height - _ONE - _MARGIN, "pos_y fora a direita do realm"

        return self._list_map_iten[pos_x][pos_y]

    def get_list_empty(self):
        list_empty = []
        for pos_x in range(self._width):
            for pos_y in range(self._height):
                if self._list_map_iten[pos_x][pos_y] == _ZERO:
                    list_empty.append([pos_x, pos_y])
        return list_empty

    def is_in_realm(self, pos_x: int, pos_y: int):
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert isinstance(pos_y, int), "type(pos_y) != int"

        response = False
        if pos_x >= _MARGIN and pos_x <= self._width - _ONE - _MARGIN:
            if pos_y >= _MARGIN and pos_y <= self._height - _ONE - _MARGIN:
                response = True
        return response

    def is_empty(self, pos_x: int, pos_y: int):
        # logging.info(f'{"[Realm] -> is_empty: inicio ..."}')
        # logging.info(f'{"[Realm] -> is_empty: "}{" "}{pos_x}{" "}{pos_y}')
        # dado posicao da coord -> retorna True quando item = 0 (zero representa vazio)
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert pos_y <= self._height - _ONE - _MARGIN, "pos_y fora a direita do realm"

        return self._list_map_iten[pos_x][pos_y] == _ZERO

    def is_add_agent(self, pos_x: int, pos_y: int, cod_agent: int):
        # adiciona novo item no mapa -> True item add ou False se local estiver != ZERO
        # logging.info(            f'{"[REALM] -> is_add_agent:"}{" "}{pos_x}{" "}{pos_y}{" "}{cod_agent}'        )
        # logger("[REALM] -> is_add_agent:", pos_x, pos_y, cod_agent)
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert pos_y <= self._height - _ONE - _MARGIN, "pos_y fora a direita do realm"

        response = False
        if cod_agent in self._list_type_agent:
            if self.is_empty(pos_x, pos_y):
                self._list_map_iten[pos_x][pos_y] = cod_agent
                response = True
        # logging.info(f'{"[REALM] -> is_add_agent: agente adicionado: "}{" "}{response}')
        return response

    def delete_item(self, breed: int, pos_x: int, pos_y: int):
        # logging.info(            f'{"[REALM] -> delete_item: "}{" "}{breed}{" "}{pos_x}{" "}{pos_y}'        )
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert pos_y <= self._height - _ONE - _MARGIN, "pos_y fora a direita do realm"

        assert isinstance(breed, int), "type(pos_y) != int"
        assert breed <= len(self._list_type_agent), "breed < self._list_type_agent"

        self._list_map_iten[pos_x][pos_y] = _ZERO
        self._list_mov += [[breed, None, None, pos_x, pos_y]]

    # Processo dinamico de atualizacao pra cada agent, pode ser q nao funcione! necessario testar
    # Outra forma é definir uma fila (lista) de atualizacao
    # Atualiza cada movimento de agentes no mapa
    def is_update(self, breed: int, pos_x: int, pos_y: int, fut_x: int, fut_y: int):
        # logging.info(            f'{"[REALM] -> is_update: "}{" "}{breed}{" "}{pos_x}{" "}{pos_y}{" "}{fut_x}{" "}{fut_y}'        )
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert pos_y <= self._height - _ONE - _MARGIN, "pos_y fora a direita do realm"

        assert isinstance(fut_x, int), "type(pos_x) != int"
        assert fut_x >= _MARGIN, "pos_x abaixo do realm"
        assert fut_x <= self._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert fut_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert fut_y <= self._height - _ONE - _MARGIN, "pos_y fora a direita do realm"

        assert isinstance(breed, int), "type(pos_y) != int"
        assert breed <= len(self._list_type_agent), "breed > self._list_type_agent"

        response = False
        if breed in self._list_type_agent:
            # logging.info(f'{"[REALM] -> is_update: breed "}{" "}{breed}')
            # logging.info(                f'{"[REALM] -> is_update: ANTES alteracao update:"}{" "}{self._list_map_iten[pos_x][pos_y]}{" "}{self._list_map_iten[fut_x][fut_y]}{" "}{pos_x}{" "}{pos_y}{" "}{fut_x}{" "}{fut_y}'            )
            self._list_map_iten[fut_x][fut_y] = breed
            self._list_map_iten[pos_x][pos_y] = _ZERO
            #################logging.info(f'{"[REALM] -> is_update: ANTES alteracao update:"}{" "}{self._list_map_iten[pos_x][pos_y]}{" "}{self._list_map_iten[fut_x][fut_y]}{" "}{pos_x}{" "}{pos_y}{" "}{fut_x}{" "}{fut_y}'            )
            self._list_mov += [[breed, pos_x, pos_y, fut_x, fut_y]]
            response = True

        return response

    def rel_total_iten_value(self):
        lin = self._width
        col = self._height
        valor_iten = _ZERO  # tipo do iten 0,1,2,3,4

        if len(self._list_iten) != (len(self._list_type_agent) + _ONE):
            # popular list_iten com agentes existentes
            for b in range(len(self._list_type_agent)):
                self._list_iten.append(self._list_type_agent[b])
            # add 0 ao total de de BREED
            for i in range(len(self._list_iten)):
                self._list_iten[i].append(_ZERO)
        else:
            for i in range(len(self._list_iten)):
                self._list_iten[i][_TWO] = 0

        # preenchendo total elementos
        for l in range(lin):
            for c in range(col):
                valor_iten = self._list_map_iten[l][c]  # 0,1,2,3
                self._list_iten[valor_iten][_TWO] += _ONE

        return self._list_iten  # list_tot_iten

    def catastrofe():
        # apaga um pedaço de mapa
        return "BOOM!!!"
