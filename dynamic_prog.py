import math

def calculate_distance(x1, y1, x2, y2):
    # Euclidean distance
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_fare(base_fare, distance, surge_multiplier):
    return base_fare + (distance * surge_multiplier)

def allocate_resources(passenger_location, driver_locations, rush_hour):
    n = len(passenger_location)  
    m = len(driver_locations)  
    base_fare = 5.0  # Base fare

    time_efficiency_table = [[0] * m for _ in range(n)]

    # time efficiency between each passenger and driver
    for i in range(n):
        for j in range(m):
            x1, y1 = passenger_location[i]
            x2, y2 = driver_locations[j]
            distance = calculate_distance(x1, y1, x2, y2)
            time_efficiency_table[i][j] = distance * 1000  # Convert distance to milliseconds

    chosen_drivers = []
    total_fares = []

    if rush_hour:
        surge_multipliers = [1.5, 2.0, 1.8] 
        fare_type = "Rush Hour"
    else:
        surge_multipliers = [1.0, 1.0, 1.0] 
        fare_type = "Non-Rush Hour"

    for i in range(n):
        min_time_efficiency = float('inf')
        chosen_driver = None
        for j in range(m):
            time_efficiency = time_efficiency_table[i][j]
            if time_efficiency < min_time_efficiency:
                min_time_efficiency = time_efficiency
                chosen_driver = j
        chosen_drivers.append(chosen_driver)

        distance = calculate_distance(
            passenger_location[i][0], passenger_location[i][1],
            driver_locations[chosen_driver][0], driver_locations[chosen_driver][1]
        )
        surge_multiplier = surge_multipliers[chosen_driver]

        fare = calculate_fare(base_fare, distance, surge_multipliers[chosen_driver])

        total_fares.append(fare)
        print(f"Passenger {i+1}: Chosen Driver {chosen_driver+1} | Total Fare: ${fare:.2f}")

    print("\n")
    print("Efficiency Table (ms):")
    for row in time_efficiency_table:
        print([f"{time:.2f}" for time in row])
    print()

# Example
passenger_location = [(0, 0), (2, 3), (5, 1)] 
driver_locations = [(1, 1), (3, 2), (4, 0)]

print("Rush Hour")
allocate_resources(passenger_location, driver_locations, rush_hour=True)

print("\nNon-Rush Hour")
allocate_resources(passenger_location, driver_locations, rush_hour=False)
