from re import L
from rutgersdelivery import __version__
from rutgersdelivery.helpers import *
import numpy as np


def test_version():
    assert __version__ == '0.1.0'


def test_validate_password1():
    password = 'rurahrah'
    assert True == validate_password(password)


def test_validate_password2():
    password = 'password'
    assert False == validate_password(password)


def test_create_destination_list():
    coordinateMap = {"Food Distribution Hub": (5, 5),
                     "Tacoria": (6, 6),
                     "Halal Guys": (6, 7),
                     "Hansel n Griddle": (7, 8),
                     "Tatas Pizza": (9, 9),
                     "Judys Kitchen": (8, 8),
                     "Cafe West": (6, 9),
                     "The Yard": (7, 9),
                     "Brower Commons": (9, 8),
                     "Panera Bread": (8, 6),
                     "Busch Dining Hall": (4, 6),
                     "Smoothie Bar": (4, 7),
                     "Woodys": (3, 8),
                     "Kilmers Market": (3, 3),
                     "Henrys Diner": (2, 2),
                     "Rutgers Cinema": (2, 4),
                     "Livingston Dining Hall": (4, 4),
                     "Neilson Dining Hall": (7, 3),
                     "Harvest": (8, 4),
                     "Cook Douglass Student Center": (9, 2),
                     "Truck Depot": (10, 10)}
    correctValue = ["Food Distribution Hub",
                    "Tacoria",
                    "Halal Guys",
                    "Hansel n Griddle",
                    "Tatas Pizza",
                    "Judys Kitchen",
                    "Cafe West",
                    "The Yard",
                    "Brower Commons",
                    "Panera Bread",
                    "Busch Dining Hall",
                    "Smoothie Bar",
                    "Woodys",
                    "Kilmers Market",
                    "Henrys Diner",
                    "Rutgers Cinema",
                    "Livingston Dining Hall",
                    "Neilson Dining Hall",
                    "Harvest",
                    "Cook Douglass Student Center",
                    "Truck Depot"]
    assert correctValue == create_destination_list(coordinateMap)


def test_get_coordinate_location():
    locations = ['Food Distribution Hub', 'Tacoria',
                 'Halal Guys', 'Hansel n Griddle', 'Truck Depot']
    expectedResult = {'Food Distribution Hub': 0, 'Tacoria': 1,
                      'Halal Guys': 2, 'Hansel n Griddle': 3, 'Truck Depot': 4}
    assert expectedResult == get_coordinate_location(locations)


def test_get_distance():
    point1 = [2, 3]
    point2 = [6, 9]
    assert 10 == get_distance(point1, point2)


def test_insert_dummy1():  # Normal Case
    start = 'Food Distribution Hub'
    coordinateLocations = {'Food Distribution Hub': 0,
                           'Tacoria': 1, 'Halal Guys': 2, 'Truck Depot': 3}
    loc = [(0, 1, 2), (0, 2, 3), (0, 3, 10), (1, 2, 1), (1, 3, 8), (2, 3, 7)]
    expectedResult = [(0, 1, 2), (0, 2, 3), (0, 3, 10), (1, 2, 1), (1, 3, 8),
                      (2, 3, 7), (0, 4, 0.1), (1, 4, 100000), (2, 4, 100000), (3, 4, 0.1)]
    assert expectedResult == insert_dummy(start, loc, coordinateLocations)


def test_insert_dummy2():  # Route has 1 location in addition to Truck Depot
    start = 'Tacoria'
    coordinateLocations = {'Tacoria': 0, 'Truck Depot': 1}
    loc = [(0, 1, 8)]
    expectedResult = [(0, 1, 8), (0, 2, 0.1), (1, 2, 0.1)]
    assert expectedResult == insert_dummy(start, loc, coordinateLocations)


def test_get_correct_order1():  # Else If Branch
    coordinateMap = {"Food Distribution Hub": (5, 5),
                     "Tacoria": (6, 6),
                     "Halal Guys": (6, 7),
                     "Hansel n Griddle": (7, 8),
                     "Tatas Pizza": (9, 9),
                     "Judys Kitchen": (8, 8),
                     "Cafe West": (6, 9),
                     "The Yard": (7, 9),
                     "Brower Commons": (9, 8),
                     "Panera Bread": (8, 6),
                     "Busch Dining Hall": (4, 6),
                     "Smoothie Bar": (4, 7),
                     "Woodys": (3, 8),
                     "Kilmers Market": (3, 3),
                     "Henrys Diner": (2, 2),
                     "Rutgers Cinema": (2, 4),
                     "Livingston Dining Hall": (4, 4),
                     "Neilson Dining Hall": (7, 3),
                     "Harvest": (8, 4),
                     "Cook Douglass Student Center": (9, 2),
                     "Truck Depot": (10, 10)}
    route = np.array([2, 1, 0])
    last = 2
    indexes = {'Food Distribution Hub': 0, 'Tacoria': 1, 'Truck Depot': 2}
    correctValue = [0, 1, 2]
    assert correctValue == get_correct_order(
        route, last, indexes, coordinateMap)


def test_get_correct_order2():  # If Branch
    coordinateMap = {"Food Distribution Hub": (5, 5),
                     "Tacoria": (6, 6),
                     "Halal Guys": (6, 7),
                     "Hansel n Griddle": (7, 8),
                     "Tatas Pizza": (9, 9),
                     "Judys Kitchen": (8, 8),
                     "Cafe West": (6, 9),
                     "The Yard": (7, 9),
                     "Brower Commons": (9, 8),
                     "Panera Bread": (8, 6),
                     "Busch Dining Hall": (4, 6),
                     "Smoothie Bar": (4, 7),
                     "Woodys": (3, 8),
                     "Kilmers Market": (3, 3),
                     "Henrys Diner": (2, 2),
                     "Rutgers Cinema": (2, 4),
                     "Livingston Dining Hall": (4, 4),
                     "Neilson Dining Hall": (7, 3),
                     "Harvest": (8, 4),
                     "Cook Douglass Student Center": (9, 2),
                     "Truck Depot": (10, 10)}
    route = np.array([0, 2, 4, 3, 1, 5])
    last = 5
    indexes = {'Food Distribution Hub': 0, 'Tatas Pizza': 1, 'Tacoria': 2,
               'Hansel n Griddle': 3, 'Halal Guys': 4, 'Truck Depot': 5}
    correctValue = [0, 2, 4, 3, 1, 5]
    assert correctValue == get_correct_order(
        route, last, indexes, coordinateMap)


def test_get_correct_order3():  # Else Branch
    coordinateMap = {"Food Distribution Hub": (5, 5),
                     "Tacoria": (6, 6),
                     "Halal Guys": (6, 7),
                     "Hansel n Griddle": (7, 8),
                     "Tatas Pizza": (9, 9),
                     "Judys Kitchen": (8, 8),
                     "Cafe West": (6, 9),
                     "The Yard": (7, 9),
                     "Brower Commons": (9, 8),
                     "Panera Bread": (8, 6),
                     "Busch Dining Hall": (4, 6),
                     "Smoothie Bar": (4, 7),
                     "Woodys": (3, 8),
                     "Kilmers Market": (3, 3),
                     "Henrys Diner": (2, 2),
                     "Rutgers Cinema": (2, 4),
                     "Livingston Dining Hall": (4, 4),
                     "Neilson Dining Hall": (7, 3),
                     "Harvest": (8, 4),
                     "Cook Douglass Student Center": (9, 2),
                     "Truck Depot": (10, 10)}
    route = np.array([3, 2, 1, 0, 6, 4, 5])
    last = 6
    indexes = {'Food Distribution Hub': 0, 'Tacoria': 1, 'Halal Guys': 2,
               'Hansel n Griddle': 3, 'Tatas Pizza': 4, 'Judys Kitchen': 5, 'Truck Depot': 6}
    correctValue = [0, 3, 2, 1, 5, 4, 6]
    assert correctValue == get_correct_order(
        route, last, indexes, coordinateMap)


def test_convert_route_to_coordinates():
    coordinateMap = {"Food Distribution Hub": (5, 5),
                     "Tacoria": (6, 6),
                     "Halal Guys": (6, 7),
                     "Hansel n Griddle": (7, 8),
                     "Tatas Pizza": (9, 9),
                     "Judys Kitchen": (8, 8),
                     "Cafe West": (6, 9),
                     "The Yard": (7, 9),
                     "Brower Commons": (9, 8),
                     "Panera Bread": (8, 6),
                     "Busch Dining Hall": (4, 6),
                     "Smoothie Bar": (4, 7),
                     "Woodys": (3, 8),
                     "Kilmers Market": (3, 3),
                     "Henrys Diner": (2, 2),
                     "Rutgers Cinema": (2, 4),
                     "Livingston Dining Hall": (4, 4),
                     "Neilson Dining Hall": (7, 3),
                     "Harvest": (8, 4),
                     "Cook Douglass Student Center": (9, 2),
                     "Truck Depot": (10, 10)}
    routeInfo = ['Food Distribution Hub', 'Tacoria',
                 'Halal Guys', 'Hansel n Griddle', 'Truck Depot']
    coordinateRoute = {'Food Distribution Hub': (5, 5), 'Tacoria': (
        6, 6), 'Halal Guys': (6, 7), 'Hansel n Griddle': (7, 8), 'Truck Depot': (10, 10)}
    assert coordinateRoute == convert_route_to_coordinates(
        routeInfo, coordinateMap)


def test_generate_graph():
    dictLocations = {'Henrys Diner': 0, 'Rutgers Cinema': 1,
                     'Busch Dining Hall': 2, 'Cook Douglass Student Center': 3, 'Truck Depot': 4}
    coordinateRoute = {'Henrys Diner': (2, 2), 'Rutgers Cinema': (2, 4), 'Busch Dining Hall': (
        4, 6), 'Cook Douglass Student Center': (9, 2), 'Truck Depot': (10, 10)}
    coordinateGraph = [(0, 1, 2), (0, 2, 6), (0, 3, 7), (0, 4, 16),
                       (1, 2, 4), (1, 3, 9), (1, 4, 14), (2, 3, 9), (2, 4, 10), (3, 4, 9)]
    assert coordinateGraph == generate_graph(dictLocations, coordinateRoute)


def test_get_final_path():
    ordered = ['Henrys Diner', 'Rutgers Cinema', 'Busch Dining Hall',
               'Cook Douglass Student Center', 'Truck Depot']
    locationList = ['Henrys Diner', 'Rutgers Cinema',
                    'Busch Dining Hall', 'Cook Douglass Student Center', 'Truck Depot']
    finalRoute = ['Henrys Diner', 'Rutgers Cinema', 'Busch Dining Hall',
                  'Cook Douglass Student Center', 'Truck Depot']
    finalDistance = 24
    assert finalRoute, finalDistance == get_final_path(ordered, locationList)


def test_get_shortest_route():
    finalCoordinateGraph = [(0, 1, 2), (0, 2, 3), (0, 3, 5), (0, 4, 8), (0, 5, 6), (0, 6, 5), (0, 7, 10), (1, 2, 1), (1, 3, 3), (1, 4, 6), (1, 5, 4), (1, 6, 3), (1, 7, 8), (2, 3, 2), (2, 4, 5), (2, 5, 3), (2, 6, 2), (2, 7, 7), (
        3, 4, 3), (3, 5, 1), (3, 6, 2), (3, 7, 5), (4, 5, 2), (4, 6, 3), (4, 7, 2), (5, 6, 3), (5, 7, 4), (6, 7, 5), (0, 8, 0.1), (1, 8, 100000), (2, 8, 100000), (3, 8, 100000), (4, 8, 100000), (5, 8, 100000), (6, 8, 100000), (7, 8, 0.1)]
    routeLength = 9
    correctAnswer = np.array([2, 6, 3, 5, 4, 7, 0, 1])
    functionOutput = get_shortest_route(finalCoordinateGraph, routeLength)
    functionOutput2 = functionOutput[functionOutput != (routeLength - 1)]
    assert np.all(correctAnswer == functionOutput2)


def test_route_beautify():
    route = ['Food Distribution Hub', 'Judys Kitchen',
             'Cafe West', 'Halal Guys', 'Hansel n Griddle']
    assert beatify_route(
        2, route) == "\033[95m Shortest Route for Truck 2: Food Distribution Hub -> Judys Kitchen -> Cafe West -> Halal Guys ->  Hansel n Griddle \033[0m"


def test_gas_calculation():
    assert gas_cost(12, 2.20) == 26.4
