from getpass import getpass
import pyinputplus as pyip
import constants as c
import helpers

# Rutgers Delivery System 
print(c.bcolors.HEADER + "Welcome to the Rutgers Delivery System. Please enter the application password to continue (See README for password)", c.bcolors.ENDC)

# Verify Password
passwordValidated = False
while passwordValidated is False:
    # Prompt User for Password
    password = getpass()

    passwordValidated = helpers.validate_password(password)

# Verify Correct Values of Routes and Trucks
trucksforRoutes = False
while trucksforRoutes is False:
    # Get Truck and Route Information
    print(c.bcolors.BOLD, "How Many Trucks are Available?", c.bcolors.ENDC)
    amountOfTrucks = pyip.inputNum()
    print(c.bcolors.BOLD, "How Many Routes are Required?", c.bcolors.ENDC)
    amountofRoutes = pyip.inputNum()

    trucksforRoutes = helpers.validate_trucks_and_routes(amountOfTrucks, amountofRoutes)

# Collect Gas Price
print(c.bcolors.BOLD, "What is the current price-per-gallon of gas?", c.bcolors.ENDC)
gasPrice = pyip.inputNum()


# Collect Routes and Calculate Shortest Path
finalRoutes = []
finalCost = 0.0
totalDistance = 0.0
for truck in range(trucksforRoutes):
    # Create a List of Valid Destinations
    validDestinations = helpers.create_destination_list(c.coordinateMap)
    validDestinations.append("END ROUTE SELECTION")

    # Ask User to Create Route for Truck
    routeInfo = helpers.get_route_info(truck, validDestinations)

    # Get Dictionary of Locations
    dictLocations = helpers.get_coordinate_location(routeInfo)

    # Get Route Locations as Dict
    coordinateRoute = helpers.convert_route_to_coordinates(routeInfo, c.coordinateMap)

    # Generate Weighted Graph
    coordinateGraph = helpers.generate_graph(dictLocations, coordinateRoute)

    # Insert Dummy Node to Graph
    finalCoordinateGraph = helpers.insert_dummy(
        routeInfo[0], coordinateGraph, dictLocations)
    
    # Get the Optimal Route (Including Dummy Node)
    optimalRoute = helpers.get_shortest_route(
        finalCoordinateGraph, len(routeInfo)+1)
    optimalRoute = optimalRoute[optimalRoute != len(routeInfo)]

    # Reorder Route with Starting and End Location (Without Dummy Node)
    optimalRouteOrdered = helpers.get_correct_order(
        optimalRoute, len(routeInfo)-1, dictLocations, c.coordinateMap)

    # Get Location Names and Total Path Distance
    finalRoute, finalDistance = helpers.get_final_path(
        optimalRouteOrdered, routeInfo, c.coordinateMap)

    # Beautify Route Information and Calculate Gas Prices
    outputRoute = helpers.beatify_route(truck+1, finalRoute)
    outputDistance = c.bcolors.BOLD + " Distance: " + str(finalDistance) + " " + c.bcolors.ENDC
    routeCost = helpers.gas_cost(finalDistance, gasPrice)
    outputCost = c.bcolors.BOLD + " Gas Price: $" + str(routeCost) + " " + c.bcolors.ENDC

    print (outputRoute, outputCost, outputDistance)
    totalDistance += finalDistance
    finalCost+=routeCost
    finalRoutes.append(outputRoute + " " + outputCost + " " + outputDistance)

print()
print("Final Routes:")
for route in finalRoutes:
    print(route)
print("Final Cost: $" + str(round(finalCost,2)))
print("Final Distance: " + str(totalDistance))

