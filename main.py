# Created By Ho Dang Manh SE181501
import math
import heapq
import time

class Airport:
    def __init__(self, ID, airport_type):
        self.id = ID
        self.airport_type = airport_type

    def __str__(self):

        return f"{self.id} {self.airport_type:>29}"

class Flight:
    def __init__(self, departure, destination, aircraft_type):
        self.departure = departure
        self.destination = destination
        self.aircraft_type = aircraft_type

class WeightedGraph:
    def __init__(self):
        self.adj = {} # adjacency list
        self.mapping = {} # mapping airportID to object airport
        self.num_aiport = 0 # number of airports

    def addAirport(self, new_airport):
        if new_airport not in self.adj:
            self.adj[new_airport] = {}
            self.num_aiport += 1
            return True
        else:
            return False

    def addRoute(self, first_airport, second_airport, cost):
        if first_airport not in self.adj:
            return False
        if second_airport not in self.adj:
            return False
        self.adj[first_airport][second_airport] = cost
        self.adj[second_airport][first_airport] = cost
        return True

    def deleteAirport(self, deleted_airport):
        if deleted_airport not in self.adj:
            return False
        # Get list neighbors of the deleted_airport
        list_neighbors = self.adj[deleted_airport]
        # Delete all routes that connected to deleted_airport
        for neighbor in list_neighbors:
            self.adj[neighbor].pop(deleted_airport)
        # Delete deleted_airport in mapping and adjacency list
        self.mapping.pop(deleted_airport)
        self.adj.pop(deleted_airport)
        return True

    def deleteRoute(self, firstAirport, secondAirport):
        if firstAirport not in self.adj: # There is no first airport
            return False
        if secondAirport not in self.adj: # There is no second airport
            return False
        if firstAirport not in self.adj[secondAirport]: # There is no route between first and second
            return False
        self.adj[firstAirport].pop(secondAirport)
        self.adj[secondAirport].pop(firstAirport)
        return True
    def updateAirportType(self, airportID):
        newType = input("Enter Airport's new type: ").upper()
        if self.isValidType(newType):
            if airportID not in self.adj:
                return False
            else:
                self.mapping[airportID].airport_type = newType
                return True
        else:
            print(f"{newType} is unavailable!!!")
            return False

    def updateAirportWeight(self, airportID):
        if airportID not in self.adj:
            return False
        list_neighbors = list(self.adj[airportID])
        for neighbor in list_neighbors:
            newCost = float(input(f"Enter new weight ({airportID}, {neighbor}): "))
            self.adj[airportID][neighbor] = newCost
            self.adj[neighbor][airportID] = newCost
        return True

    # First Display (Just show information of a list of Airports)
    def showListAirport(self):
        for airport in self.adj:
            print(self.mapping[airport])
    # Second Display (Show information Airports and neighbors of them)

    def showAdjacencyList(self):
        for airport in self.adj:
            print(f'Adjacency List of {airport}')
            print(f'{airport} -> ', end=' ')
            list_neighbors = list(self.adj[airport].items())
            for i in range(len(list_neighbors)):
                if i != len(list_neighbors) - 1:
                    print(f'{list_neighbors[i]} -> ', end=' ')
                else:
                    print(f'{list_neighbors[i]}', end=' ')
            print()

    def calculateCost(self, flight):
        shortest_distance, _ = self.dijkstra(flight)
        return shortest_distance

    def findTheShortestRoute(self, flight):
        start = flight.departure
        end = flight.destination
        shortest_distance, trace = self.dijkstra(flight)
        if shortest_distance == float('inf'):
            print("There is no path!!!!")
            return
        path = []
        current_node = end
        while current_node != start:
            path.insert(0, current_node)
            current_node = trace[current_node]
        path.insert(0, start)
        print("The Shortest Path: ", end=' ')
        for i in range(len(path) - 1):
            print(f'{path[i]} -> ', end=' ')
        print(f'{path[-1]}')

    def dijkstra(self, flight):
        start = flight.departure
        end = flight.destination
        visited = set()
        d = {airport: float('inf') for airport in self.adj}
        d[start] = 0
        priorityQueue = [(d[start], start)]
        heapq.heapify(priorityQueue)
        trace = {start: start}
        while priorityQueue:
            distance, current_node = heapq.heappop(priorityQueue)
            visited.add(current_node)
            for neighbor, weight in self.adj[current_node].items():
                if not self.isValidRoute(flight.aircraft_type, self.mapping[neighbor].airport_type):
                    visited.add(neighbor)
                    continue
                if neighbor not in visited:
                    if d[neighbor] > d[current_node] + weight:
                        d[neighbor] = d[current_node] + weight
                        trace[neighbor] = current_node
                        heapq.heappush(priorityQueue, (d[neighbor], neighbor))
        return d[end], trace

    def boomb(self):
        self.adj = {}
        self.mapping = {}
        self.num_aiport = 0
    def isValidRoute(self, aircraftType, airportType):
        status = None
        if aircraftType == 'S':
            status = True
        elif aircraftType == 'M':
            if airportType != 'S':
                status = True
            else:
                status = False
        else:
            if airportType == 'L':
                status = True
            else:
                status = False
        return status

    def isValidType(self, type):
        if type in ['L', 'M', 'S']:
            return True
        return False

    def isValidAirport(self, airportID):
        if airportID not in self.adj:
            return True
        return False

    def isValidOption(self, listOptions, choice):
        if choice in listOptions:
            return True
        return False
def menu():
    print("-".center(50, '-'))
    print('|' + "List of options".center(48) + '|')
    print("-".center(50, '-'))
    print('1. Add an airport'.center(50))
    print('2. Add a route.'.center(50))
    print('3. Delete an airport.'.center(50))
    print('4. Delete a route.'.center(50))
    print('5. Update an airport.'.center(50))
    print('6. List airports and their networks.'.center(50))
    print('7. Calculate cost.'.center(50))
    print('8. Find the shortest route.'.center(50))
    print('9. Bomb!!!!!!!!!!!!!!!!!'.center(50))
    print("-" .center(50, '-'))

if __name__ == '__main__':
    #--------------------------------------- BEGIN -----------------------------------------#
    graph = WeightedGraph()

    while True:
        menu()
        action = input("Enter your choice: ")
        if graph.isValidOption(['1', '2', '3', '4', '5', '6', '7', '8', '9'], action):
            if action == '1': # Add airport
                AirportID = input("Enter airport's ID: ").upper()
                if graph.isValidAirport(AirportID):
                    Airport_type = input("Enter airport's type (L/M/S): ").upper()
                    if graph.isValidType(Airport_type):
                        airport = Airport(AirportID, Airport_type)
                        graph.mapping[AirportID] = airport
                        check = graph.addAirport(AirportID)
                        if check:
                            print(f'Add an airport {AirportID} successfully!!!')
                        else:
                            print(f'Add an airport {AirportID} unsuccessfully!!!')
                    else:
                        print(f'Unsuccesfully, {Airport_type} is unvailable!!!')
                else:
                    print(f'Unsuccessfully, airport {AirportID} is already exists!!!')

            elif action == '2': # Add route
                if graph.num_aiport < 2:
                    print("There must be at least 2 airports!!!")
                    continue
                fromAirportID = input("Enter the first airport's ID: ").upper()
                toAirportID = input("Enter the second airport's ID: ").upper()
                if fromAirportID != toAirportID:
                    cost = float(input("Enter the cost between 2 airports: "))
                    check = graph.addRoute(fromAirportID, toAirportID, cost)
                    if check:
                        print("Add a route successfully!!!")
                    else:
                        notExistAirport = None
                        if fromAirportID not in graph.adj:
                            notExistAirport = fromAirportID
                        else:
                            notExistAirport = toAirportID
                        print(f"Unsuccessfully, airport {notExistAirport} does not exist!!!!")
                else:
                    print("You have just inputed 2 identical airport, please input again!!!!")
            elif action == '3': # Delete airport
                deleted_airportID = input("Enter airport's ID: ").upper()
                checkDelete = graph.deleteAirport(deleted_airportID)
                if checkDelete:
                    print("Delete succesfully!!!")
                else:
                    print(f"Unsuccessfully, airport {deleted_airportID} does not exist!!!!")
            elif action == '4': # Delete route
                firstAirport = input("Enter first airport's ID: ").upper()
                secondAirport = input("Enter second airport's ID: ").upper()
                checkDelete = graph.deleteRoute(firstAirport, secondAirport)
                if checkDelete:
                    print("Delete succesfully!!!")
                else:
                    notExistAirport2 = None
                    if firstAirport not in graph.adj:
                        notExistAirport2 = firstAirport
                    elif secondAirport not in graph.adj:
                        notExistAirport2 = secondAirport
                    else:
                        print(f"The route between {firstAirport} and {secondAirport} does not exist!!!")
                        continue
                    print(f"Unsuccessfully, airport {notExistAirport2} does not exist!!!!")
            elif action == '5':
                # Update's options
                updated_airportID = input("Enter airport's ID: ").upper()
                print("1. Update airport's type")
                print("2. Update airport's weight to others")
                print("3. Update airport's type and airport's weight to others")
                choose = input("Enter your choice: ")
                if graph.isValidOption(['1', '2', '3'], choose):
                    if choose == '1':
                        checkUpdate = graph.updateAirportType(updated_airportID)
                        if checkUpdate:
                            print("Update successfully!!!")
                        else:
                            print(f"Unsuccessfully, airport {updated_airportID} does not exist!!!!")
                    elif choose == '2':
                        checkUpdate = graph.updateAirportWeight(updated_airportID)
                        if checkUpdate:
                            if checkUpdate:
                                print("Update successfully!!!")
                            else:
                                print(f"Unsuccessfully, airport {updated_airportID} does not exist!!!!")
                    else:
                        checkUpdate = graph.updateAirportType(updated_airportID) and graph.updateAirportWeight(updated_airportID)
                        if checkUpdate:
                            print("Update successfully!!!")
                        else:
                            print(f"Unsuccessfully, airport {updated_airportID} does not exist!!!!")
                else:
                    print(f'Option {choose} is unavailble!!!')

            elif action == '6': # Traversal List Airport
                print("List of Airports".center(50, '-'))
                print("Airport's ID", "Airport's Type".rjust(31))
                graph.showListAirport()
                print()
                print("Adjacency List of each Airport".center(50, '-'))
                graph.showAdjacencyList()
            elif action in ['7', '8']:
                departure = input("Enter your departure: ").upper()
                destination = input("Enter your destination: ").upper()
                aircraftType = input("Enter aircraft's type: ").upper()
                aircraft = Flight(departure, destination, aircraftType)
                departureType = graph.mapping[departure].airport_type
                destinationType = graph.mapping[destination].airport_type
                if graph.isValidRoute(aircraftType, departureType) and graph.isValidRoute(aircraftType, destinationType):
                    if action == '7':
                        shortestCost = graph.calculateCost(aircraft)
                        if shortestCost == float('inf'):
                            print("There is no path!!!")
                        else:
                            print(f'Shortest Cost: {graph.calculateCost(aircraft)}')
                    else: # action = 8
                        graph.findTheShortestRoute(aircraft)
                else:
                    print("There is no path!!!!")
                    continue
            else:
                print("Do you really want to bomb into the world?")
                print('1. Yes')
                print('2. No')
                action2 = input("Enter your final choice: ")
                if graph.isValidOption(['1', '2'], action2):
                    if action2 == '1':
                        print('Human will be died in', end=' ')
                        time.sleep(1)
                        print(3, end=' ')
                        time.sleep(1)
                        print(2, end=' ')
                        time.sleep(1)
                        print(1,end=' ')
                        time.sleep(1)
                        print('Bomb!!!!!!!!!!!!!')
                        print('See you in the heaven')
                        exit()
                    else:
                        continue
                else:
                    print(f'Option {action2} is unavailble!!!')
        else:
            print(f'Option {action} is unavailble!!!')
    # --------------------------------------- END -----------------------------------------#