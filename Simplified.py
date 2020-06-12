import tkinter as tk
import os
import random
import math
from PIL import Image

towns = []

#Proyecto creado por Hernan Castillo,Jesús García,Juan Gomez y Daniel Paz
class Town:

    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return 'Town: ' + self.name + '\tX: ' + \
               str(self.x) + '\tY: ' + str(self.y)

#obtener puntajes
def get_score(town_a, town_b):
    x1 = town_a.x
    x2 = town_b.x
    y1 = town_a.y
    y2 = town_b.y
    return 1/math.pow(x2-x1,2)+math.pow(y2-y2,2)

#clase de las rutas
class Route:

    def __init__(self, route):
        self.route = []
        for town in route:
            self.route.append(towns[town])

    def append(self, town):
        self.route.append(town)

    def remove(self, route):
        for town in route:
            self.route.remove(town)

    def get_fitness(self):
        fitness = 0
        for i in range(len(self.route)-1):
            fitness += get_score(self.route[i], self.route[i+1])
        return fitness

    def splice(self, start, end):
        return Route(self.route[start:end])

    def __len__(self):
        return len(self.route)


def greed(route_a, route_b):
    start = random.randint(1, len(route_a)-3)
    if route_a.splice(start, start+3).get_fitness() > route_b.splice(start, start+3).get_fitness():
        splice = route_a.splice(start, start+3)
        route_c = list(route_b)
        route_c.remove(splice)
        route_c.append(splice)
    else:
        splice = route_b.splice(start, start + 3)
        route_c = list(route_a)
        route_c.remove(splice)
        route_c.append(splice)
    return route_c


def envy(route_a, route_b):
    start = random.randint(1, len(route_a)-3)
    if route_a.splice(start, start+3).get_fitness() < route_b.splice(start, start+3).get_fitness():
        splice = route_a.splice(start, start+3)
        route_c = list(route_b)
        route_c.remove(splice)
        route_c.append(splice)
    else:
        splice = route_b.splice(start, start + 3)
        route_c = list(route_a)
        route_c.remove(splice)
        route_c.append(splice)
    return route_c

#funciones de los 7 pecados capitales
def sloth(route_a):
    return route_a


def wrath(route_a):
    return random.sample(list(route_a), k=len(route_a))


def lust(route_a, route_b):
    route_c = []
    return route_c


for town_id in range(10):
    towns.append(Town(random.random()*1000, random.random()*1000))
routes = []
eksdi = list(range(10))
routes.append(Route(eksdi))
for new_route in range(9):
    routes.append(Route(random.sample(eksdi, len(eksdi))))
best_routes = []
for picked_town in towns:
    print(picked_town)
for one in range(2):
    best_route = routes[0]
    print(best_route)
    route_fitness = best_route.get_fitness()
    for picked_route in routes:
        picked_fitness = picked_route.get_fitness()
        if picked_fitness > route_fitness:
            route_fitness = picked_fitness
            best_route = picked_route
    routes.remove(best_route)
    best_routes.append(best_route)

