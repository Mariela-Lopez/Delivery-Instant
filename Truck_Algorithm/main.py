# Mariela Mendoza Lopez (Student ID: )

from hash_table import HashTable
from package import Package
import csv

package_table = HashTable()


def loadPackageData():
    with open("CSV/package_data.csv", encoding='utf-8-sig') as package_data:
        package_data_csv = csv.reader(package_data, delimiter=",")

        first_truck_packages = []
        second_truck_packages = []
        third_truck_packages = []

        for package_row in package_data_csv:
            id_number = int(package_row[0])
            address = package_row[1]
            city = package_row[2]
            state = package_row[3]
            zip_code = package_row[4]
            deliveryDeadline = package_row[5]
            massKilo = package_row[6]
            note = package_row[7]

            package = Package(id_number, address, city, state, zip_code, deliveryDeadline, massKilo, note)
            package_table.insert(id_number, package)

            if package.id == 2 or package.id == 4 or package.id == 5 or package.id == 7 or package.id == 8 or package.id == 9 or package.id == 10 or package.id == 11 or package.id == 12 or package.id == 17 or package.id == 21 or package.id == 22 or package.id == 23 or package.id == 24 or package.id == 26 or package.id == 27:
                third_truck_packages.append(package.id)

                continue

            if package.id == 1 or package.id == 13 or package.id == 14 or package.id == 15 or package.id == 16 or package.id == 19 or package.id == 20 or package.id == 29 or package.id == 30 or package.id == 31 or package.id == 34 or package.id == 37 or package.id == 40:
                first_truck_packages.append(package.id)

                continue

            if package.id == 3 or package.id == 6 or package.id == 18 or package.id == 25 or package.id == 28 or package.id == 32 or package.id == 33 or package.id == 35 or package.id == 36 or package.id == 38 or package.id == 39:
                second_truck_packages.append(package.id)
                continue

        return package_table, first_truck_packages, second_truck_packages, third_truck_packages


def loadDistances():
    with open("CSV/addresses_file_csv.csv", encoding='utf-8-sig', newline='') as addresses_file, open(
            "CSV/address_distances.csv", encoding='utf-8-sig', newline='') as distances_file:
        addresses_file_csv = csv.reader(addresses_file, delimiter=",")
        distances_file_csv = csv.reader(distances_file, delimiter=",")
        addresses = list(addresses_file)
        distances = list(distances_file_csv)
        addresses_stripped = list(map(lambda a: a.strip(), addresses))

        return addresses_stripped, distances


package_table, first_truck_packages, second_truck_packages, third_truck_packages = loadPackageData()
addresses, distances = loadDistances()


def get_truck_path_algorithm(truck_package_ids, initial_time):
    current_time = initial_time
    current_location_index = 0
    delivery_order = []
    package_distances = []
    delivery_times = []
    total_distance = 0
    while len(truck_package_ids) != 0:
        closest_package_id = get_closest_package_id(current_location_index, truck_package_ids)
        package_index = get_package_index_by_package_id(closest_package_id, truck_package_ids)
        delivery_order.append(closest_package_id)
        truck_package_ids.pop(package_index)
        next_location_index = get_address_index(package_table.get(closest_package_id).address)
        distance = getDistance(current_location_index, next_location_index)
        package_distances.append(distance)
        current_location_index = next_location_index
        time_taken = get_time_for_distance_in_minutes(distance)
        total_distance = distance + total_distance

        delivery_times.append(time_taken)
        # current_time = update_time(current_time, time_taken)
    print("Delivery Order by Package ID")
    print(delivery_order)
    print("Distance for each delivery")
    print(package_distances)
    print("Time taken for each delivery")
    print(delivery_times)

    print("Total distance for truck")
    print(total_distance)

    return current_time


def get_time_for_distance_in_minutes(distance):
    return (distance / 16) * 60


def getDistance(first_location_index, second_location_index):
    distance = distances[first_location_index][second_location_index]
    if distance == "":
        return float(distances[second_location_index][first_location_index])
    return float(distance)


def get_closest_package_id(current_location_index, truck_package_ids):
    closest_package_id = -1
    min_distance = 99999999
    for package_id in truck_package_ids:
        package = package_table.get(package_id)
        address = package.address
        address_index = get_address_index(address)
        package_distance = getDistance(current_location_index, address_index)
        if package_distance < min_distance:
            min_distance = package_distance
            closest_package_id = package_id

    return closest_package_id


def get_closest_package_location(truck_package_ids):
    closest_package_id = -1
    for package_id in truck_package_ids:
        package = package_table.get(package_id)
        address = package.address
        address_index = get_address_index(address)

    return closest_package_id


def get_address_index(address):
    return [i for i in range(len(addresses)) if address in addresses[i]][0]


def get_package_index_by_package_id(package_id, package_list):
    return [i for i in range(len(package_list)) if package_id == package_list[i]][0]


print("TRUCK1")
finished_time1 = get_truck_path_algorithm(first_truck_packages, "")
print("TRUCK2")
finished_time2 = get_truck_path_algorithm(second_truck_packages, "")
print("TRUCK3")
finished_time3 = get_truck_path_algorithm(third_truck_packages, finished_time2)
