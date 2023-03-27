# -*- coding: utf-8 -*-

import random
import math
from realm import Realm

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
_BREED = [[0, "empty"], [1, "plant"], [2, "prey"], [3, "predator"]]


class Plant:
    """  is a class for mathematical operations on complex numbers.

        Attributes:
        real (int): The real part of complex number.
        imag (int): The imaginary part of complex number.
    """

    def __init__(self, realm, age_limit=50):

        assert isinstance(realm, object), "type(realm) != object"
        assert isinstance(age_limit, int), "type(age_limit) != int"
        assert age_limit >= _ZERO, "age_limit < zero"

        self._realm = realm
        self._age_limit = age_limit

        self._breed = _BREED[_ONE][_ZERO]  # plant
        self._age = _ZERO
        self._is_alive = True

        self._coord_x = None
        self._coord_y = None

        # criacao plant
        list_el_candidate = self._realm.get_list_empty()

        while len(self._realm.get_list_empty()) != _ZERO:

            el_candidate = random.choice(list_el_candidate)

            if self._realm.is_add_agent(
                el_candidate[_ZERO], el_candidate[_ONE], self._breed
            ):
                self._coord_x = el_candidate[_ZERO]
                self._coord_y = el_candidate[_ONE]
                self._realm._list_mov.append(
                    [
                        self._breed,
                        self._coord_x,
                        self._coord_y,
                        self._coord_x,
                        self._coord_y,
                    ]
                )
                break

        if not (isinstance(self._coord_x, int) or isinstance(self._coord_y, int)):
            self._is_alive = False
            # raise Exception("Realm Full")

    def is_update(self):

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

        assert isinstance(self._breed, int), "type(age_limit) != int"
        assert self._breed <= len(_BREED), "breed > len(_BREED)"
        response = False
        self._age += _ONE
        if self._is_alive:
            response = True
            if self._age > self._age_limit:
                self.delete()
        return response

    def delete(self):

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

        self._realm.delete_item(self._breed, self._coord_x, self._coord_y)
        self._is_alive = False
        self._age = self._age_limit + _ONE

    def is_alive(self):
        # logging.info(f'{"[Plant] -> is_alive: inicio ..."}')
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

        # logging.info(            f'{"[Plant] -> is_alive:"}{" "}{self._coord_x}{" "}{self._coord_y}'        )
        response = True

        # necessario para apagar na lista de update
        if self._realm.get_type_iten(self._coord_x, self._coord_y) != self._breed:
            # logging.info(                f'{"[Plant] -> self._realm.get_type_iten(pos_x , pos_y) != self._breed"}'            )
            self.is_alive = False

        if self._age > self._age_limit:
            # logging.info(f'{"[Plant] -> is_alive: self._age > self._age_limit"}')
            self.is_alive = False

        if self.is_alive == False:
            self._realm.delete_item(self._breed, self._coord_x, self._coord_y)
            response = False

        # logging.info(f'{"[Plant] -> is_alive:"}{" "}{response}')
        # logging.info(f'{"[Plant] -> is_alive: ... fim"}')
        return response
