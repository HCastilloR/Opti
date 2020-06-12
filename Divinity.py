import random
import math

towns = []
routes = []


class Town:

    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return str(self.name)


def get_score(town_a, town_b):
    x1 = town_a.x
    x2 = town_b.x
    y1 = town_a.y
    y2 = town_b.y
    return 1/math.pow(x2-x1, 2)+math.pow(y2-y2, 2)


def get_fitness(route):
    score = 0
    for i in range(len(route)-1):
        score += get_score(route[i], route[i+1])
    return score


def generate_towns():
    for town_id in range(10):
        towns.append(Town(random.random() * 1000, random.random() * 1000, name=town_id))


def generate_routes():
    first_list = []
    for town_id in towns:
        first_list.append(town_id)
    routes.append(first_list)
    for i in range(9):
        routes.append(random.sample(first_list, k=len(first_list)))


def print_town_list(town_list):
    string_list = '['
    for town in town_list:
        string_list += str(town) + ', '
    print(string_list[:len(string_list)-2] + ']')


def remove_from_route(route, splice):
    for any_town in splice:
        route.remove(any_town)


def append_to_route(route, splice):
    for any_town in splice:
        route.append(any_town)


def greed(route_a, route_b):
    start = random.randint(1, len(route_a)-3)
    if get_fitness(route_a[start:start + 3]) > get_fitness(route_b[start:start + 3]):
        splice = route_a[start:start+3]
        route_c = list(route_b)
    else:
        splice = route_b[start:start + 3]
        route_c = list(route_a)
    remove_from_route(route_c, splice)
    append_to_route(route_c, splice)
    return route_c


def envy(route_a, route_b):
    start = random.randint(1, len(route_a)-3)
    if get_fitness(route_a[start:start + 3]) < get_fitness(route_b[start:start + 3]):
        splice = route_a[start:start+3]
        route_c = list(route_b)
    else:
        splice = route_b[start:start + 3]
        route_c = list(route_a)
    remove_from_route(route_c, splice)
    append_to_route(route_c, splice)
    return route_c


def sloth(route_a):
    return route_a


def wrath(route_a):
    return random.sample(routes[0], k=len(routes[0]))


def magic_happens():
    # Picking the best two routes
    best_routes = []
    for one in range(2):
        best_route = routes[0]
        route_fitness = get_fitness(routes[0])
        for any_route in routes:
            picked_fitness = get_fitness(any_route)
            if picked_fitness > route_fitness:
                route_fitness = picked_fitness
                best_route = any_route
        routes.remove(best_route)
        best_routes.append(best_route)
    # Removing all the other routes
    routes.clear()
    for any_route in best_routes:
        print('Chosen route: ', end='')
        print_town_list(any_route)
        routes.append(any_route)
    # Breeding new routes
    for i in range(2):
        routes.append(greed(routes[0], routes[1]))
        routes.append(envy(routes[0], routes[1]))
        routes.append(sloth(routes[i]))
        routes.append(wrath(routes[i]))


generate_towns()
generate_routes()
for generation in range(10):
    print('Generation: ' + str(generation))
    magic_happens()

