import random
import math
from PIL import Image, ImageDraw

towns = []
routes = []
ellipse_radius = 10
generation = 1
log_file = open('log.txt', 'w')


class Town:

    def __init__(self, x, y, name=""):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return 'Town: ' + str(self.name) + ' at x: ' + str(self.x) + '\ty: ' + str(self.y)

    def print_number(self):
        return str(self.name)


def get_distance(town_a, town_b):
    x1 = town_a.x
    x2 = town_b.x
    y1 = town_a.y
    y2 = town_b.y
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))


def get_fitness(route):
    score = 0
    for i in range(len(route) - 1):
        score += get_distance(route[i], route[i + 1])
    return 1/score


def generate_towns():
    for town_id in range(10):
        towns.append(Town(random.random() * 600, random.random() * 600, name=town_id))


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
        string_list += town.print_number() + ', '
    return string_list[:len(string_list) - 2] + ']'


def remove_from_route(route, splice):
    for any_town in splice:
        route.remove(any_town)


def append_to_route(route, splice):
    for any_town in splice:
        route.append(any_town)


def greed(route_a, route_b):
    start = random.randint(1, len(route_a) - 3)
    if get_fitness(route_a[start:start + 3]) > get_fitness(route_b[start:start + 3]):
        splice = route_a[start:start + 3]
        route_c = list(route_b)
    else:
        splice = route_b[start:start + 3]
        route_c = list(route_a)
    remove_from_route(route_c, splice)
    append_to_route(route_c, splice)
    return route_c


def envy(route_a, route_b):
    start = random.randint(1, len(route_a) - 3)
    if get_fitness(route_a[start:start + 3]) < get_fitness(route_b[start:start + 3]):
        splice = route_a[start:start + 3]
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
    # Log all routes
    log_file.write('All routes:\n')
    log_routes()
    log_file.write('\n')
    # Picking the best two routes
    best_routes = []
    log_file.write('Best routes:\n')
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
        log_file.write(print_town_list(best_route) + '\n')
    # Removing all the other routes
    routes.clear()
    log_file.write('\n')
    for any_route in best_routes:
        routes.append(any_route)
    # Breeding new routes
    for i in range(2):
        routes.append(greed(routes[0], routes[1]))
        routes.append(envy(routes[0], routes[1]))
        routes.append(sloth(routes[i]))
        routes.append(wrath(routes[i]))
    # Generational output
    for i in range(2):
        output = Image.new('RGB', (600, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(output)
        for any_town in towns:
            x = any_town.x
            y = any_town.y
            draw.ellipse((x - ellipse_radius, y - ellipse_radius,
                          x + ellipse_radius, y + ellipse_radius),
                         fill='blue', outline='red')
        for index in range(len(best_routes[i]) - 1):
            x1 = best_routes[i][index].x
            y1 = best_routes[i][index].y
            x2 = best_routes[i][index + 1].x
            y2 = best_routes[i][index + 1].y
            draw.line((x1, y1, x2, y2), width=3, fill='black')
        for any_town in towns:
            x = any_town.x
            y = any_town.y
            draw.text((x, y - ellipse_radius / 2), str(any_town.name), color='black', fill='white')
        output.save('Generation ' + str(generation) + ' Best route ' + str(i) + '.jpg')


def generate_map():
    output = Image.new('RGB', (600, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(output)
    for any_town in towns:
        x = any_town.x
        y = any_town.y
        draw.ellipse((x - ellipse_radius, y - ellipse_radius,
                      x + ellipse_radius, y + ellipse_radius),
                     fill='blue', outline='red')
        draw.text((x, y - ellipse_radius / 2), str(any_town.name), color='black', fill='white')
    output.save('map.jpg')


def log_towns():
    log_file.write('Towns:\n')
    for any_town in towns:
        log_file.write(str(any_town) + '\n')


def log_routes():
    for any_route in routes:
        log_file.write(print_town_list(any_route) + '\n')


generate_towns()
log_towns()
generate_routes()
log_file.write('\nStarting routes:\n')
log_routes()
log_file.write('\n')
generate_map()
for generation in range(10):
    log_file.write('Generation: ' + str(generation) + '\n')
    magic_happens()
log_file.close()
