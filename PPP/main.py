# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 13:44:49 2023

@author: beLIVE

4320p (8K): 7680 x 4320.
2160p (4K): 3840 x 2160.
1440p (2K): 2560 x 1440.
1080p (HD): 1920 x 1080.
720p (HD): 1280 x 720.
480p (SD): 854 x 480.
360p (SD): 640 x 360.
240p (SD): 426 x 240.
"""


import matplotlib.pyplot as plt


import time, datetime
import random, math
import numpy as np

import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter

from realm import Realm
from plant import Plant
from agent import Prey, Predator

from parameters import REALM_WIDTH, REALM_HEIGHT


import logging

logging.basicConfig(
    filename="ppp.log",
    filemode="w",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)

_WIDTH = 640  # tamanho largura tela
_HEIGHT = 360  # tamanho altura tela


def main():

    f = open("grafico.csv", "w")
    print(0, ",", "Title", ",", "Model Prey Predator / Pthon", file=f)

    print("Criando realm ...")

    map = Realm(_WIDTH, _HEIGHT)
    print("... Realm criado")
    # map = Realm(15, 15)

    print("Criando os agentes ...")
    # plants = [Plant(map) for p in range(200)]
    # preys = [Prey(map) for b in range(50)]
    # predators = [Predator(map) for c in range(50)]

    plants = [Plant(map) for p in range(300)]
    preys = [Prey(map) for b in range(60)]
    predators = [Predator(map) for c in range(40)]
    print("... Agentes criados")

    timestep = 0
    list_timestep = []
    count_empty = []
    count_plant = []
    count_prey = []
    count_predator = []

    while timestep < 10000 and (
        len(plants) + len(preys) + len(predators) <= _WIDTH * _HEIGHT
    ):
        print(f'{"[Step]: "}{timestep}')

        # print("1: ",len(plants),len(preys),len(predators))
        print(
            f'{"[Step]: Verificando saúde"}{" "}{len(plants)}{" "}{len(preys)}{" "}{len(predators)}'
        )
        plants = [p for p in plants if p.is_alive()]
        preys = [p for p in preys if p.is_alive()]
        predators = [p for p in predators if p.is_alive()]

        # update
        # print("2: ",len(plants),len(preys),len(predators))
        print(
            f'{"[Step]: update"}{" "}{len(plants)}{" "}{len(preys)}{" "}{len(predators)}'
        )
        [c.is_update() for c in preys]
        [c.is_update() for c in predators]
        [c.is_update() for c in plants]

        print(
            f'{"[Step]: Verificando saúde"}{" "}{len(plants)}{" "}{len(preys)}{" "}{len(predators)}'
        )
        plants = [p for p in plants if p.is_alive()]
        preys = [p for p in preys if p.is_alive()]
        predators = [p for p in predators if p.is_alive()]

        print(
            f'{"[Step]: reprocriacao"}{" "}{len(plants)}{" "}{len(preys)}{" "}{len(predators)}'
        )
        for p in preys:
            if p._energy >= 30:
                p._energy += 5
                preys = preys + [Prey(map)]

        for p in predators:
            if p._energy >= 50:
                p._energy += 5
                predators = predators + [Predator(map)]

        total_seed = random.randrange(0, 50)
        for i in range(total_seed):
            plants = plants + [Plant(map)]

        # print("Depois len(plants),len(preys),len(predators): ",len(plants),len(preys),len(predators))
        # [print(timestep, ',', 'Position',  ',', 'Plant', ',', a._coord_x, ',', a._coord_y, file=f) for a in plants]
        # [print(timestep, ',', 'Position',  ',', 'Prey', ',', a._coord_x, ',', a._coord_y, file=f) for a in preys]
        # [print(timestep, ',', 'Position',  ',', 'Plant', ',', a._coord_x, ',', a._coord_y, file=f) for a in predators]

        # val_rel = [len(plants),len(preys),len(predators)]
        val_rel = [len(plants), len(preys), len(predators)]
        # print(val_rel)

        # lista para gráficos
        # list_cont_var = map.rel_total_iten_value()

        list_timestep += [timestep]
        count_plant += [val_rel[0]]
        count_prey += [val_rel[1]]
        count_predator += [val_rel[2]]

        # proximo

        timestep = timestep + 1
    logging.info(f'{"[Main] -> map._list_mov"}{map._list_mov}')
    logging.info(f'{"[Main] -> map._list_mov"}{map._list_mov}')
    t = list_timestep
    x = count_plant
    y = count_prey
    z = count_predator
    # print("len(t), len(x), len(y):", len(t), len(x), len(y))

    plt.plot(t, x, label="line plant", color="green")
    plt.plot(t, y, label="line prey", color="blue")
    plt.plot(t, z, label="line predator", color="red")

    # , marker='+'

    plt.title("unemployment rate vs year", fontsize=14)

    plt.xlabel("year", fontsize=14)
    plt.ylabel("unemployment rate", fontsize=14)

    plt.legend()
    plt.grid(True)

    # plt.ylim(0, 20)
    plt.xlim(0, 500)
    # plt.xticks(range(1, 10000))#sombrear
    # plt.gcf().set_size_inches(50, 25)

    plt.show()
    print("Grafico Plotado!!")

    # print("Total plants, preys: ",  len(predators),  file=f)
    # print(*map._list_map_iten , sep="\n")


if __name__ == "__main__":
    main()
