# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:05:31 2023

@author: beLIVE
"""

import random
import math
from realm import Realm
from plant import Plant

import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter


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
_THREE = 3
_FOUR = 4
_BREED = [[0, "empty"], [1, "plant"], [2, "prey"], [3, "predator"]]


l = open("log.csv", "w")
print(0, ",", "Title", ",", "Model Prey Predator / Python", file=l)


class Agent:
    def __init__(self, realm, initial_energy, ray, age_limit, breed, food, value_food):
        assert isinstance(realm, object), "type(realm) != object"
        assert isinstance(initial_energy, int), "type(initial_energy) != int"
        assert initial_energy >= _ZERO, "initial_energy < zero"
        assert isinstance(ray, int), "type(ray) != int"
        assert ray >= _ZERO, "ray < zero"
        assert isinstance(age_limit, int), "type(age_limit) != int"
        assert age_limit >= _ZERO, "age_limit < zero"
        assert isinstance(breed, int), "type(age_limit) != int"
        assert breed <= len(_BREED), "breed > len(_BREED)"
        assert breed >= _ZERO, "breed < _ZERO"
        assert isinstance(food, int), "type(food) != int"
        assert food >= _ZERO, "food < zero"
        assert isinstance(value_food, int), "type(value_food) != int"
        assert value_food >= _ZERO, "value_food < zero"

        self._realm = realm
        self._initial_energy = initial_energy
        self._ray = ray
        self._ray_ini = ray
        self._age_limit = age_limit
        self._breed = breed
        self._food = food
        self._value_food = value_food
        self._age = _ZERO
        self._energy = initial_energy
        self._is_alive = True
        self._coord_x = None
        self._coord_y = None

        # criacao agente
        list_el_candidate = self._realm.get_list_empty()
        while len(self._realm.get_list_empty()) != _ZERO:

            el_candidate = random.choice(list_el_candidate)
            if self._realm.is_add_agent(
                el_candidate[_ZERO], el_candidate[_ONE], self._breed
            ):
                self._coord_x = el_candidate[_ZERO]
                self._coord_y = el_candidate[_ONE]
                self._realm._list_mov += [
                    [
                        self._breed,
                        self._coord_x,
                        self._coord_y,
                        self._coord_x,
                        self._coord_y,
                    ]
                ]
                break

        # #logging.info(f'{"[Agent] -> criado:"}{" "}{self._breed}{" "}{el_candidate}')
        if not (isinstance(self._coord_x, int) or isinstance(self._coord_y, int)):
            self._is_alive = False
            self._realm._list_mov += [[breed, None, None, None, None]]
            # raise Exception("Realm Full")

    def get_coord(self):
        return [self._coord_x, self._coord_y]

    def delete(self, breed: int, pos_x: int, pos_y: int):
        # logging.info(f'{"[Agent] -> delete: inicio ..."}')
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._realm._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            pos_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"

        assert isinstance(breed, int), "type(age_limit) != int"
        assert breed <= len(_BREED), "breed > len(_BREED)"

        self._realm.delete_item(self._breed, pos_x, pos_y)
        # logging.info(            f'{"[Agent] -> delete "}{" "}{self._breed}{" "}{pos_x}{" "}{pos_y}'        )
        # logging.info(f'{"[Agent] -> is_reproduce: ... fim"}')

    # Reproducao de agente retorna proposta de nova coordenada
    # atenção necessario tirar energia no update

    def reproduce(self, var_dist_rep=2):
        # logging.info(f'{"[Agent] -> _reproduce: inicio ..."}')
        assert isinstance(self._coord_x, int), "type(pos_x) != int"
        assert self._coord_x >= _MARGIN, "pos_x abaixo do realm"
        assert (
            self._coord_x <= self._realm._width - _ONE - _MARGIN
        ), "pos_x acima do realm"

        assert isinstance(self._coord_y, int), "type(pos_y) != int"
        assert self._coord_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            self._coord_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"
        assert isinstance(var_dist_rep, int), "type(var_dist_rep) != object"
        assert var_dist_rep > _ZERO, "var_dist_rep <= zero"

        list_reproduce = []
        coord_reproduce = []
        new_coords = None

        list_rep = self._radar(var_dist_rep, _ZERO)

        if isinstance(list_rep, list) and len(list_rep) != _ZERO:
            coord_reproduce = random.choice(list_rep)
            new_coords = [coord_reproduce[_ZERO], coord_reproduce[_ONE]]

        # logging.info(f'{"[Agent] -> reproduce "}{" "}{coord_reproduce}')
        # logging.info(f'{"[Agent] -> is_reproduce: ... fim"}')
        return new_coords

    def is_eat(self, pos_x, pos_y):
        # logging.info(f'{"[Agent] -> _eat: inicio ..."}')
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._realm._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            pos_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"

        assert isinstance(self._breed, int), "type(age_limit) != int"
        assert self._breed <= len(_BREED), "breed > len(_BREED)"

        response = False
        type_pos = self._realm.get_type_iten(pos_x, pos_y)
        # logging.info(  f'{"[Agent] -> is_eat: verifica se nova posicao NAO esta vazia"}{" "}{pos_x}{" "}{pos_y}'        )
        if not self._realm.is_empty(pos_x, pos_y):
            # logging.info( f'{"[Agent] -> is_eat: nova posicao NAO esta vazia"}{" "}{pos_x}{" "}{pos_y}'            )
            if self._realm.is_update(
                self._breed, self._coord_x, self._coord_y, pos_x, pos_y
            ):

                # logging.info(                    f'{"[Agent] -> is_eat: update ok"}{" "}{self._coord_x}{" "}{self._coord_y}{" "}{pos_x}{" "}{pos_y}'                )
                self._realm._list_mov += [[type_pos, pos_x, pos_y, None, None]]
                self._coord_x = pos_x
                self._coord_y = pos_y
                self._energy += self._value_food
                response = True

        # logging.info(f'{"[Agent] -> is_eat: "}{" "}{self._coord_x}{" "}{self._coord_y}')
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._realm._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            pos_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"
        # logging.info(f'{"[Agent] -> is_eat: ... fim"}')
        return response

    def is_move(self, pos_x, pos_y):
        # logging.info(f'{"[Agent] -> _move: inicio ..."}')
        # logging.info(f'{"[Agent] -> is_move: inicio "}{" "}{pos_x}{" "}{pos_y}')
        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._realm._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            pos_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"

        assert isinstance(self._breed, int), "type(age_limit) != int"
        assert self._breed <= len(_BREED), "breed > len(_BREED)"

        response = False
        f'{"[Agent] -> is_move: verifica se acha local vazio"}{" "}{pos_x}{" "}{pos_y}'
        if self._realm.is_empty(pos_x, pos_y):
            # logging.info(                f'{"[Agent] -> is_move: achou local vazio"}{" "}{pos_x}{" "}{pos_y}'            )
            if self._realm.is_update(
                self._breed, self._coord_x, self._coord_y, pos_x, pos_y
            ):
                # logging.info(f'{"[Agent] -> is_move: moveu"}{" "}{pos_x}{" "}{pos_y}')
                self._coord_x = pos_x
                self._coord_y = pos_y
                self._energy -= _ONE
                response = True
        else:
            f'{"[Agent] -> is_move: nao achou local vazio"}{" "}{"tentar processo randomico"}'
            list_ran = [0] * 6 + [1] * 2 + [-1] * 2
            rx = list_ran[random.randrange(0, 10)]
            ry = list_ran[random.randrange(0, 10)]
            f'{"[Agent] -> is_move: proposta randomica"}{" "}{pos_x + rx}{" "}{pos_y + ry}'
            if self._realm.is_in_realm(pos_x + rx, pos_y + ry):
                f'{"[Agent] -> is_move: esta no realm"}{" "}{pos_x + rx}{" "}{pos_y + ry}'
                if self._realm.is_empty(pos_x + rx, pos_y + ry):
                    if self._realm.is_update(
                        self._breed,
                        self._coord_x,
                        self._coord_y,
                        pos_x + rx,
                        pos_y + ry,
                    ):
                        # logging.info(                            f'{"[Agent] -> is_move: random, moveu para"}{" "}{pos_x + rx}{" "}{pos_y + ry}'                        )

                        self._coord_x = pos_x + rx
                        self._coord_y = pos_y + ry
                        self._energy -= _ONE
                        # logging.info(                            f'{"[Agent] -> is_move: random, moveu para"}{" "}{self._coord_x}{" "}{self._coord_y}'                        )
                        response = True
                    # else:
                    # logging.info( f'{"[Agent] -> is_move: random, nao moveu para"}{" "}{pos_x}{" "}{pos_y}'                        )

        assert isinstance(pos_x, int), "type(pos_x) != int"
        assert pos_x >= _MARGIN, "pos_x abaixo do realm"
        assert pos_x <= self._realm._width - _ONE - _MARGIN, "pos_x acima do realm"

        assert isinstance(pos_y, int), "type(pos_y) != int"
        assert pos_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            pos_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"
        # logging.info(f'{"[Agent] -> is_move: ... fim"}')
        return response

    def is_update(self):
        # logging.info(f'{"[Agent] -> _update: inicio ..."}')
        # logging.info(           f'{"[Agent] -> is_update new:"}{" "}{self._breed}{" "}{self._coord_x}{" "}{self._coord_y}'        )
        assert isinstance(self._coord_x, int), "type(pos_x) != int"
        assert self._coord_x >= _MARGIN, "pos_x abaixo do realm"
        assert (
            self._coord_x <= self._realm._width - _ONE - _MARGIN
        ), "pos_x acima do realm"

        assert isinstance(self._coord_y, int), "type(pos_y) != int"
        assert self._coord_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            self._coord_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"

        # limite do radar
        # esse relatorio pode ajudar self._realm.rel_total_iten_value()[1][2] > ZERO

        fx = 0
        fy = 0

        list_target = []
        target_dist = None
        target_x = None
        target_y = None
        var_eat = False
        var_move = False

        list_target = self._hunt()
        # print("list_target", list_target)
        assert isinstance(list_target, list), "isinstance(list_target) != list"

        # Se existe pelo menos 1 alvo _E_ o alvo é comida
        if (
            len(list_target) == _FOUR
            and self._realm.get_type_iten(list_target[_TWO], list_target[_THREE])
            == self._food
        ):
            # logging.info(f'{"[Agent] -> in update: achou algum alvo"}')

            target_dist = list_target[_ZERO]
            target_x = list_target[_TWO]
            target_y = list_target[_THREE]

            # Se o agent esta vivo
            if self._is_alive == True:
                # logging.info(f'{"[Agent] -> in update: achou algum alvo"}')

                # Se o alvo esta com distacia igual 1, somente comer
                if target_dist == _ONE:
                    # logging.info(f'{"[Agent] -> in update: achou algum alvo"}')
                    if self.is_eat(target_x, target_y):
                        # logging.info(f'{"[Agent] -> in update: achou algum alvo"}')
                        var_eat = True
                        self._energy -= _ONE
                        self._ray = self._ray_ini

                # Se o alvo esta com distacia maior 1, criar vetor velocidade
                else:
                    # logging.info(f'{"[Agent] -> in update: achou algum alvo"}')
                    var_eat = False

                    # contrucao do vetor direcao
                    if target_x - self._coord_x > _ZERO:
                        fx = 1
                    else:
                        fx = -1
                    list_ran_x = [fx] * 9 + [_ZERO] * 1
                    # aleatoriedade da casa _ZERO
                    fx = list_ran_x[random.randrange(0, 10)]

                    if target_y - self._coord_y > _ZERO:
                        fy = 1
                    else:
                        fy = -1
                    list_ran_y = [fy] * 9 + [_ZERO] * 1
                    # aleatoriedade da casa _ZERO
                    fy = list_ran_y[random.randrange(0, 10)]

                    # construcao vetor deslocamento dx, dy
                    dx = self._coord_x + fx
                    dy = self._coord_y + fy

                    # Se a movimentacao obteve sucesso
                    # logging.info(                        f'{"[Agent] -> is_update: mover para alvo"}{" "}{self._coord_x}{" "}{self._coord_y}{" "}{dx}{" "}{dy}'                   )
                    # logging.info(f'{"[Agent] -> is_update : verifica se esta no mapa"}')
                    if self._realm.is_in_realm(dx, dy):
                        # logging.info(                            f'{"[Agent] -> is_update: esta no mapa, verifica se vai se mover"}'                        )
                        if self.is_move(dx, dy):
                            # logging.info(f'{"[Agent] -> is_update: moveu para alvo"}')
                            var_move = True
                            self._energy -= _ONE
                        else:
                            # logging.info(   f'{"[Agent] -> is_update: dx, dy fora do realm"}{" "}{self._coord_x}{" "}{self._coord_y}{" "}{dx}{" "}{dy}'                         )
                            var_move = False
                            self._ray += 1

            else:
                # logging.info(f'{"[Agent] -> is_update: O agente esta morto"}')
                var_eat = False
                var_move = False

        # Se nao existir alvo
        else:
            # logging.info(f'{"[Agent] -> is_update: nao achou alvo, Raio + 1"}')
            var_eat = False
            var_move = False
            self._ray += 1
            self._energy -= _ONE

        self._age += _ONE
        # logging.info(            f'{"[Agent] -> is_update: ... fim"}{" "}{self._breed}{" "}{self._coord_x}{" "}{self._coord_y}'        )
        return var_eat or var_move

    def _hunt(self):
        # logging.info(f'{"[Agent] -> _hunt: inicio ..."}')
        assert isinstance(self._coord_x, int), "type(pos_x) != int"
        assert self._coord_x >= _MARGIN, "pos_x abaixo do realm"
        assert (
            self._coord_x <= self._realm._width - _ONE - _MARGIN
        ), "pos_x acima do realm"

        assert isinstance(self._coord_y, int), "type(pos_y) != int"
        assert self._coord_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            self._coord_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"

        target = []
        list_dist_target = []

        # Captura lista de alvos do radar
        list_target = self._radar(self._ray, self._food)
        assert isinstance(list_target, list), "isinstance(list_target) != list"
        # print("In hunt -> list_target", list_target)

        # Caso exista elemento list_target retornar o de menor distancia
        if len(list_target) > _ZERO:

            for t in range(len(list_target)):
                assert isinstance(
                    list_target[t][_ZERO], int
                ), "type(list_target[t][ZERO]) != int"
                assert (
                    list_target[t][_ZERO] >= _MARGIN
                ), "list_target[t][ZERO] abaixo do realm"
                assert (
                    list_target[t][_ZERO] <= self._realm._width - _ONE - _MARGIN
                ), "list_target[t][ZERO] acima do realm"

                assert isinstance(
                    list_target[t][_ONE], int
                ), "list_target[t][_ONE] != int"
                assert (
                    list_target[t][_ONE] >= _MARGIN
                ), "list_target[t][_ONE] abaixo do realm"
                assert (
                    list_target[t][_ONE] <= self._realm._height - _ONE - _MARGIN
                ), "list_target[t][_ONE] acima do realm"

                dist_square = round(
                    math.sqrt(
                        (list_target[t][_ZERO] - self._coord_x) ** _TWO
                        + (list_target[t][_ONE] - self._coord_y) ** _TWO
                    )
                )
                list_dist_target.append(
                    [dist_square, list_target[t][_ZERO], list_target[t][_ONE]]
                )

            # print("In hunt ->: list_dist_target:", list_dist_target)
            target_less_dist = random.choice(list_dist_target)

            # print("In hunt ->: target_less_dist:", target_less_dist)
            for dist in list_dist_target:
                if target_less_dist[_ZERO] > dist[_ZERO]:
                    # print(target_less_dist)
                    target_less_dist = dist

            # ordena lista em relacao a distancia
            # list_dist_target = sorted(list_dist_target, key=itemgetter(_ZERO))

            # Criar target
            target = [
                target_less_dist[_ZERO],
                self._food,
                target_less_dist[_ONE],
                target_less_dist[_TWO],
            ]

            # print("In hunt ->: target montado: ", target)
        # logging.info(f'{"[Agent] -> _hunt:"}{" "}{target}')
        # logging.info(f'{"[Agent] -> _hunt: ... fim"}')
        return target

    def _radar(self, ray, search_for):
        # logging.info(f'{"[Agent] -> _radar: inicio ..."}')
        assert isinstance(self._coord_x, int), "type(pos_x) != int"
        assert self._coord_x >= _MARGIN, "pos_x abaixo do realm"
        assert (
            self._coord_x <= self._realm._width - _ONE - _MARGIN
        ), "pos_x acima do realm"

        assert isinstance(self._coord_y, int), "type(pos_y) != int"
        assert self._coord_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            self._coord_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"

        assert isinstance(ray, int), "type(ray) != int"
        assert ray > _ZERO, "ray <= _ZERO"

        list_target = []
        var_search = search_for
        list_ray = []
        list_pos_x = []
        list_pos_y = []
        l_x = []
        l_y = []
        px = None
        py = None

        # calcula conjunto de direcoes
        for r in range(ray + _ONE):
            list_ray.append(-r)
            list_ray.append(r)
        list_ray = list(set(sorted(list_ray)))

        # Calcula abrangencia do raio
        for r in list_ray:

            if (
                self._coord_x + r >= _MARGIN
                and self._coord_x + r <= self._realm._width - _ONE - _MARGIN
            ):
                px = self._coord_x + r
            else:
                px = self._coord_x

            assert isinstance(px, int), "type(px) != int"
            if px >= _MARGIN and px <= self._realm._width - _ONE - _MARGIN:
                list_pos_x.append(px)

            if (
                self._coord_y + r >= _MARGIN
                and self._coord_y + r <= self._realm._height - _ONE - _MARGIN
            ):
                py = self._coord_y + r
            else:
                py = self._coord_y

            assert isinstance(py, int), "type(py) != int"
            if py >= _MARGIN and py <= self._realm._height - _ONE - _MARGIN:
                list_pos_y.append(py)

        ##logging.info(            f'{"[Agent] -> _radar: coordenadas candidatas"}{" "}{l_x}{" "}{l_y}'        )
        # Ordena e retira os iguais
        list_pos_x = list(set(sorted(list_pos_x)))
        list_pos_y = list(set(sorted(list_pos_y)))
        # logging.info(            f'{"[Agent] -> _radar: lista de coordenadas"}{" "}{list_pos_x}{" "}{list_pos_y}'        )

        # print("In radar: list_pos_x, list_pos_y ", list_pos_x, list_pos_y)
        # retira elementos None
        for xi in range(len(list_pos_x)):
            if isinstance(list_pos_x[xi], int):
                l_x += [list_pos_x[xi]]
        for yi in range(len(list_pos_y)):
            if isinstance(list_pos_y[yi], int):
                l_y += [list_pos_y[yi]]

        ##logging.info(            f'{"[Agent] -> _radar: coordenadas candidatas"}{" "}{l_x}{" "}{l_y}'        )
        # verifica se as coordenadas sao ponto de comida
        for lx in l_x:
            for ly in l_y:
                if self._realm.is_in_realm(lx, ly):
                    # logging.info(                        f'{"[Agent] -> _radar: verifica _realm.get_type_iten() "}{" "}{l_x}{" "}{l_y}'                    )
                    if self._realm.get_type_iten(lx, ly) == var_search:
                        list_target.append([lx, ly])

        # print("list_target.append([lx,ly]): ", list_target)
        assert isinstance(list_target, list), "list_target != list"
        ##logging.info(f'{"[Agent] -> _radar:"}{" "}{list_target}')
        ##logging.info(f'{"[Agent] -> _radar: ... fim"}')
        return list_target

    def is_alive(self):
        ##logging.info(f'{"[Agent] -> is_alive: inicio ..."}')
        assert isinstance(self._coord_x, int), "type(pos_x) != int"
        assert self._coord_x >= _MARGIN, "pos_x abaixo do realm"
        assert (
            self._coord_x <= self._realm._width - _ONE - _MARGIN
        ), "pos_x acima do realm"

        assert isinstance(self._coord_y, int), "type(pos_y) != int"
        assert self._coord_y >= _MARGIN, "pos_y fora a esquerda do realm"
        assert (
            self._coord_y <= self._realm._height - _ONE - _MARGIN
        ), "pos_y fora a direita do realm"

        response = True
        ##logging.info(            f'{"[Agent] -> is_alive:"}{" "}{self._coord_x}{" "}{self._coord_y}'        )
        # if self._realm.is_in_realm(self._coord_x, self._coord_y):
        #    response = False
        # else:
        if self._age > self._age_limit:
            # logging.info(f'{"[Agent] -> is_alive: self._age > self._age_limit"}')
            self.is_alive = False
        if self._energy < _ZERO:
            # logging.info(f'{"[Agent] -> is_alive: self._energy < self._age_limit"}')
            self.is_alive = False

        if self.is_alive == False:
            # logging.info(                f'{"[Agent] -> is_alive: chama delete"}{" "}{self._breed}{" "}{self._coord_x}{" "}{self._coord_y}'            )
            self.delete(self._breed, self._coord_x, self._coord_y)
            response = False
        ##logging.info(f'{"[Agent] -> is_alive:"}{" "}{response}')
        ##logging.info(f'{"[Agent] -> is_alive: ... fim"}')
        return response


class Prey(Agent):
    def __init__(
        self, realm, energy=20, ray=1, age_limit=100, breed=2, food=1, valor_food=10
    ):
        super().__init__(realm, energy, ray, age_limit, breed, food, valor_food)
        # self.age_limit = age_limit


class Predator(Agent):
    def __init__(
        self, realm, energy=20, ray=1, age_limit=50, breed=3, food=2, valor_food=10
    ):
        super().__init__(realm, energy, ray, age_limit, breed, food, valor_food)
        # self.age_limit = age_limit
