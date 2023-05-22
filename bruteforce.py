import math
from itertools import permutations

def calculate_distance(x1, y1, x2, y2):
    # Euclidean distance
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def allocate_resources_brute_force(passenger_location, driver_locations):
    n = len(passenger_location) 
    m = len(driver_locations) 

    min_total_time_efficiency = float('inf')
    best_allocation = None

    # all possible permutations of drivers
    driver_permutations = permutations(range(m))

    # Iterate through each permutation
    for permutation in driver_permutations:
        total_time_efficiency = 0
        for i in range(n):
            passenger_index = i
            driver_index = permutation[i]
            x1, y1 = passenger_location[passenger_index]
            x2, y2 = driver_locations[driver_index]
            distance = calculate_distance(x1, y1, x2, y2)
            time_efficiency = distance * 1000
            total_time_efficiency += time_efficiency

        if total_time_efficiency < min_total_time_efficiency:
            min_total_time_efficiency = total_time_efficiency
            best_allocation = list(permutation)

    return best_allocation


passenger_location = [(0, 0), (2, 3), (5, 1)]  
driver_locations = [(1, 1), (3, 2), (4, 0)] 

best_allocation = allocate_resources_brute_force(passenger_location, driver_locations)

print("Brute Force Solution:")
for i, passenger in enumerate(passenger_location):
    chosen_driver = best_allocation[i]
    driver = driver_locations[chosen_driver]
    print(f"Passenger {i+1} Location: {passenger}")
    print(f"Chosen Driver: Driver {chosen_driver+1} Location: {driver}")
    print()
