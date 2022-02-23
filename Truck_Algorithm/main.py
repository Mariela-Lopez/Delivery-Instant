# Mariela Mendoza Lopez (Student ID: 6245034 )

import datetime
from hash_table import HashTable
from package import Package
import csv


# Initializes the package class and inserts into hashtable
# spacetime complexity -> O(n)
def loadPackageData():
    table = HashTable()
    with open("CSV/package_data.csv", encoding='utf-8-sig') as package_data:
        package_data_csv = csv.reader(package_data, delimiter=",")

        truck_packages1 = []
        truck_packages2 = []
        truck_packages3 = []

        # input the information from the CV rows into the new package object
        # spacetime complexity -> O(n)
        for package_row in package_data_csv:
            id_number = int(package_row[0])
            address = package_row[1]
            city = package_row[2]
            state = package_row[3]
            zip_code = package_row[4]
            deliveryDeadline = package_row[5]
            massKilo = package_row[6]
            note = package_row[7]

            # create new package objects
            package = Package(id_number, address, city, state, zip_code, deliveryDeadline, massKilo, note)
            table.insert(id_number, package)

            # get these package id's and put them into the three different trucks
            # spacetime complexity -> O(1)
            if package.id == 1 or package.id == 13 or package.id == 14 or package.id == 15 or package.id == 16 or \
                    package.id == 19 or package.id == 20 or package.id == 29 or package.id == 30 \
                    or package.id == 31 or package.id == 34 or package.id == 37 or package.id == 40:
                truck_packages1.append(package.id)
                continue
            # spacetime complexity -> O(1)
            if package.id == 3 or package.id == 6 or package.id == 18 or package.id == 25 or package.id == 28 or \
                    package.id == 32 or package.id == 33 or package.id == 35 or package.id == 36 or \
                    package.id == 38 or package.id == 39:
                truck_packages2.append(package.id)
                continue
            # spacetime complexity -> O(1)
            if package.id == 2 or package.id == 4 or package.id == 5 or package.id == 7 or package.id == 8 \
                    or package.id == 9 or package.id == 10 or package.id == 11 or package.id == 12 or package.id == 17 \
                    or package.id == 21 or package.id == 22 or package.id == 23 or package.id == 24 or \
                    package.id == 26 or package.id == 27:
                truck_packages3.append(package.id)
                continue

        return table, truck_packages1, truck_packages2, truck_packages3


# loads distances information from CSV files
# spacetime complexity -> 0(1)
def loadDistances():
    with open("CSV/addresses_file_csv.csv", encoding='utf-8-sig', newline='') as addresses_file, open(
            "CSV/address_distances.csv", encoding='utf-8-sig', newline='') as distances_file:
        distances_file_csv = csv.reader(distances_file, delimiter=",")
        addresses1 = list(addresses_file)
        distances1 = list(distances_file_csv)
        addresses_stripped = list(map(lambda a: a.strip(), addresses1))

        return addresses_stripped, distances1


# variables that contain the return values of the functions
# spacetime complexity -> O(n)
package_table, first_truck_packages, second_truck_packages, third_truck_packages = loadPackageData()

# spacetime complexity -> 0(1)
addresses, distances = loadDistances()


# function that adds minutes to a time
# spacetime complexity-> O(1)
def add_minutes_to_time(current_time, minutes):
    return current_time + datetime.timedelta(minutes=minutes)


# main nearest neighbor algorithm that finds the path for the truck
# spacetime complexity -> O(4n^2 * m)
def get_truck_path_algorithm(truck_package_ids, initial_time):
    current_time = initial_time
    current_location_index = 0
    total_distance = 0

    # for every id in the truck id list, get the package from the hashtable, and update the leave hub time to current
    # spacetime complexity -> O(n)
    for truck_package_id in truck_package_ids:
        package = package_table.get_package(truck_package_id)
        package.leave_hub_time = current_time

    # spacetime complexity-> O(3n^2 * m)
    while len(truck_package_ids) != 0:
        # Get package_id of package closest to current location
        # spacetime complexity of get_closest_package_id is O(n * m)
        closest_package_id = get_closest_package_id(current_location_index, truck_package_ids)

        # Get index of closest package (index in truck package ids list)
        # spacetime complexity of get_package_index_by_package_id is O(n)
        package_index = get_package_index_by_package_id(closest_package_id, truck_package_ids)

        # Remove package id from truck's package id list (already delivered)
        truck_package_ids.pop(package_index)

        # Get the delivered package's address index
        # spacetime complexity for get_address_index is O(n)
        next_location_index = get_address_index(package_table.get_package(closest_package_id).address)

        # Get the distance between the previous location and the current package's location
        distance = getDistance(current_location_index, next_location_index)

        # Calculate how long this delivery took based on the distance
        time_taken_minutes = get_time_for_distance_in_minutes(distance)

        # update the current time by adding the time taken minutes
        current_time = add_minutes_to_time(current_time, time_taken_minutes)

        package = package_table.get_package(closest_package_id)
        package.delivered_time = current_time

        # Set current_location to the last delivered package's location
        current_location_index = next_location_index
        # Add distance to total distance
        total_distance = distance + total_distance

    # Hub is address index 0 in the list
    hub_index = 0
    # Get distance from last package location to hub
    distance_to_hub = getDistance(current_location_index, hub_index)
    time_taken_minutes = get_time_for_distance_in_minutes(distance_to_hub)
    current_time = add_minutes_to_time(current_time, time_taken_minutes)

    return current_time, total_distance


# function that returns the distance calculated in minutes by 18 mph
# time complexity -> O(1)
def get_time_for_distance_in_minutes(distance):
    return (distance / 18) * 60


# returns the distances between two indexes
# time complexity -> O(1)
def getDistance(first_location_index, second_location_index):
    distance = distances[first_location_index][second_location_index]
    if distance == "":
        return float(distances[second_location_index][first_location_index])
    return float(distance)


# function that returns the closest package id from a location index
# spacetime complexity -> O(n * m)
def get_closest_package_id(current_location_index, truck_package_ids):
    closest_package_id = -1
    min_distance = 99999999

    # for every package in the truck package id's check to see which one has the least distance
    # spacetime complexity -> O(n * m)
    for package_id in truck_package_ids:
        package = package_table.get_package(package_id)
        address = package.address

        # time complexity of get_address_index -> O(m)
        address_index = get_address_index(address)
        package_distance = getDistance(current_location_index, address_index)
        if package_distance < min_distance:
            min_distance = package_distance
            closest_package_id = package_id

    return closest_package_id


# function that returns the index of the address
# spacetime complexity -> o(m)
def get_address_index(address):
    return [i for i in range(len(addresses)) if address in addresses[i]][0]


# function that returns the index of the package based on id
# spacetime complexity -> o(n)
def get_package_index_by_package_id(package_id, package_list):
    return [i for i in range(len(package_list)) if package_id == package_list[i]][0]


# first truck leaves at 8:00 am
# spacetime complexity -> 0(1)
truck1_leave_time = datetime.timedelta(hours=8)

# executes the main algorithm for truck 1
# returns finished time and total distance traveled of truck 1
# spacetime complexity of get_truck_path_algorithm -> O(4n^3)
finished_time1, total_distance1 = get_truck_path_algorithm(first_truck_packages, truck1_leave_time)

# second truck leaves at 09:30
# spacetime complexity -> O(1)
truck2_leave_time = datetime.timedelta(hours=9, minutes=30)

# executes the main algorithm for truck 2
# returns finished time and total distance traveled of truck 2
# spacetime complexity of get_truck_path_algorithm -> O(4n^3)
finished_time2, total_distance2 = get_truck_path_algorithm(second_truck_packages, truck2_leave_time)

# executes the main algorithm for truck 3
# returns finished time and total distance traveled of truck 3
# spacetime complexity of get_truck_path_algorithm -> O(4n^3)
finished_time3, total_distance3 = get_truck_path_algorithm(third_truck_packages, finished_time2)

# adds the total distances of the three trucks and prints to the console
# spacetime complexity -> 0(1)
combined_total_distances = total_distance1 + total_distance2 + total_distance3
print(f"The total distance traveled for all 3 trucks is {combined_total_distances} miles! ")


# function that gives option to console
# spacetime complexity -> O(n)
def run_program_for_user():
    user_feature_selection = input(
        "Please choose option below. \nOption 1: Enter 1 if you would like to search by individual package. \nOption "
        "2: Enter 2 if you would like to search for all packages of a given time.")
    # if user chooses 1 then take them to the individual package option
    if user_feature_selection == "1":
        run_individual_package_feature()
    # if user chooses 2 then take him to the all packages option
    # spacetime complexity of run_all_packages feature is O(n)
    elif user_feature_selection == "2":
        run_all_packages_feature()


# function that returns individual package information based on id and time
# spacetime complexity -> O(1)
def run_individual_package_feature():
    # get the id and time from user input
    user_input_package_id = input("Package ID: ")
    user_input_time = get_converted_time(input("Time - Please use HH:MM:SS as input in military time: "))

    # get the package info from the user input id and calculate the status and info of the package
    package = package_table.get_package(int(user_input_package_id))
    package.calculate_status(user_input_time)


# function that returns all packages info based on a certain time
# spacetime complexity -> O(n)
def run_all_packages_feature():
    # get time from user input
    user_input_time = get_converted_time(input("Time: Please use HH:MM:SS as input in military time: "))

    # for every package in the hashtable calculate the status and info
    for package in package_table.getAllPackages():
        package.calculate_status(user_input_time)


# function that takes a user input string and splits it into the format needed in a timedelta
# spacetime complexity -> O(1)
def get_converted_time(user_input_time):
    (h, m, s) = user_input_time.split(':')
    user_input_time_changed = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    return user_input_time_changed


# calls the function that runs the console options for user
run_program_for_user()
