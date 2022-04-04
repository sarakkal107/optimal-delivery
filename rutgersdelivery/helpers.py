from passlib.hash import bcrypt
import pyinputplus as pyip
import mlrose_hiive as mlrose
import numpy as np
from collections import OrderedDict
from rutgersdelivery.constants import bcolors
# Validate password before entering application


def validate_password(password):
    # Hash Password
    hasher = bcrypt.using(rounds=13)
    # Compare Given Password Hash with Correct Password Hash
    applicationContinue = hasher.verify(
        password, "$2b$13$sBfW5r9Cnn6729OtbeY4J.qCqbNieBZt0ZV/dw68c3z9oFjkZPRUi")
    # Print Result Message
    if applicationContinue is False:
        print(bcolors.FAIL, "Unable to verify password. See README for correct password. Retry Below:", bcolors.ENDC)
        return False
    else:
        print(bcolors.OKGREEN,
              "Password Validated. Starting Application...", bcolors.ENDC)
        print("")
        return True

# Create List of Destinations


def create_destination_list(coordinateMap):
    validValues = []
    for destination in coordinateMap:
        validValues.append(destination)
    return validValues

# Validate that there enough trucks for routes


def validate_trucks_and_routes(amountOfTrucks, amountofRoutes):
    if amountOfTrucks < amountofRoutes:
        print(bcolors.FAIL, "There are not enough trucks for the required routes. Please make sure the amount of trucks is equal to or more than the required routes.", bcolors.ENDC)
        print(bcolors.BOLD,
              "Please input valid values of trucks and routes to continue", bcolors.ENDC)
        print("")
        return False
    elif amountOfTrucks == amountofRoutes:
        print(bcolors.OKGREEN,
              "Equivalent number of trucks and routes.", bcolors.ENDC)
        print("")
        return amountOfTrucks
    elif amountofRoutes < amountOfTrucks:
        print(bcolors.OKGREEN, "Sufficient amount of trucks supplied.",
              amountOfTrucks-amountofRoutes, "trucks will not be used.", bcolors.ENDC)
        print("")
        return amountofRoutes

# Collect Destinations in Route


def get_route_info(truck, validValues):
    print(bcolors.UNDERLINE + "Getting Route Info for Truck " + str(truck+1) + bcolors.ENDC)
    print()
    result = ""
    routeList = []
    while result != "END ROUTE SELECTION":
        print(bcolors.WARNING,
              "When finished, select 'END ROUTE SELECTION'", bcolors.ENDC)
        result = pyip.inputMenu(validValues, lettered=False, numbered=True)
        if result != "END ROUTE SELECTION":
            routeList.append(result)
        print(bcolors.OKCYAN, "Current Route List:", routeList, bcolors.ENDC)
        print("")

    # Add Truck Depot
    routeList.append("Truck Depot")
    # Filter results to remove duplicates
    filteredResult = list(OrderedDict.fromkeys(routeList))
    return filteredResult

# Create Dictionary of All Route Locations


def get_coordinate_location(locations):
    coordinateLocation = {}
    counter = 0
    for item in locations:
        coordinateLocation[item] = counter
        counter += 1
    return coordinateLocation

# Map Route to Coordinates


def convert_route_to_coordinates(routeInfo, coordinateMap):
    routeCoordinates = {}
    for destination in routeInfo:
        routeCoordinates[destination] = coordinateMap[destination]
    return routeCoordinates

# Get Distance Between Two Points


def get_distance(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])

# Generate Weighted Graph of Route


def generate_graph(coordinateLocations, coordinateMap):
    output = []
    v = list(coordinateMap.values())
    k = list(coordinateMap.keys())
    i = 0
    while (i < len(v)):
        for item in v[i+1:]:
            distance = get_distance(v[i], item)
            output.append((coordinateLocations.get(
                k[i]), coordinateLocations.get(k[v.index(item)]), distance))
        i += 1
    return output
    

# Add Dummy to Graph


def insert_dummy(start, loc, coordinateLocations):
    dummyInt = len(coordinateLocations.keys())
    for k, v in coordinateLocations.items():
        if (start == k):
            loc.append((v, dummyInt, 0.1))
        elif (k == "Truck Depot"):
            loc.append((v, dummyInt, 0.1))
        else:
            loc.append((v, dummyInt, 100000))
    return loc

# Get Shortest Path (With Dummy Node)


def get_shortest_route(dist_list, lenList):
    fitness_coords = mlrose.TravellingSales(distances=dist_list)
    problem_fit = mlrose.TSPOpt(
        length=lenList, fitness_fn=fitness_coords, maximize=False)
    best_state, best_fitness, x = mlrose.genetic_alg(
        problem_fit, random_state=2)
    return best_state

# Reorder Path with Pickup Point and Last Point (Without Dummy Node)


def get_correct_order(route, last, indexes, coordinateMap):
    orderedRoute = route.tolist()
    orderedRoute.remove(last)
    if len(orderedRoute) == 0:
        return []
    if (orderedRoute[0] == 0):
        orderedRoute.append(last)
        return orderedRoute
    elif (orderedRoute[len(orderedRoute)-1] == 0):
        orderedRoute = orderedRoute[::-1]
        orderedRoute.append(last)
        return orderedRoute
    else:
        reordered = []
        pickupPointIndex = orderedRoute.index(0)
        for k, v in indexes.items():
            if (v == orderedRoute[pickupPointIndex]):
                cur = np.asarray(coordinateMap[k])
            elif (v == orderedRoute[pickupPointIndex-1]):
                prev = np.asarray(coordinateMap[k])
            elif (v == orderedRoute[pickupPointIndex+1]):
                next = np.asarray(coordinateMap[k])
        #print(prev, cur, next)

        dist1 = np.linalg.norm(cur-prev)
        dist2 = np.linalg.norm(cur-next)
        #print(dist1, dist2)
        if (dist1 < dist2):  # ABCKUV wrong
            reordered.append(0)
            for item in orderedRoute[:pickupPointIndex]:
                reordered.append(item)
            for item in reversed(orderedRoute[pickupPointIndex+1:]):
                reordered.append(item)
            reordered.append(last)
        else:
            for item in orderedRoute[pickupPointIndex:]:
                reordered.append(item)
            for item in orderedRoute[:pickupPointIndex]:
                reordered.append(item)
            reordered.append(last)
        return reordered

# Get Path with Locations and Total Distance


def get_final_path(ordered, locationList, coordinateMap):
    output = []
    totalDistance = 0
    for index in ordered:
        output.append(locationList[index])
    cur = 0
    nex = 1
    while (nex < len(output)):
        temp = get_distance(np.asarray(coordinateMap[output[cur]]), np.asarray(
            coordinateMap[output[nex]]))
        totalDistance = totalDistance + temp
        cur += 1
        nex += 1

    return output, totalDistance

def beatify_route(truck, finalRoute):
    counter = 1
    returnString = ""
    for destination in finalRoute:
        if counter==1:
            returnString = returnString + bcolors.HEADER + " Shortest Route for Truck " + str(truck) + ": " + destination + " -> "
        elif counter==len(finalRoute):
            returnString = returnString + " " + destination + " " + bcolors.ENDC
        else:
            returnString = returnString + destination + " -> "
        counter+=1
    return returnString

def gas_cost(finalDistance, gasPrice):
    gasCost = round(finalDistance * gasPrice,2)
    return(gasCost)