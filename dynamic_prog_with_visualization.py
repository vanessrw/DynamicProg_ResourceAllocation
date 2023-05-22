import math
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

def calculate_distance(x1, y1, x2, y2):
    # Euclidean distance
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_fare(base_fare, distance, surge_multiplier):
    return base_fare + (distance * surge_multiplier)

def allocate_resources():
    passenger_location = [(60, 50), (200, 150), (320, 70)] 
    driver_locations = [(100, 100), (200, 250), (300, 100)]
    rush_hour = rush_hour_var.get()

    n = len(passenger_location) 
    m = len(driver_locations) 
    base_fare = 5.0  

    time_efficiency_table = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            x1, y1 = passenger_location[i]
            x2, y2 = driver_locations[j]
            distance = calculate_distance(x1, y1, x2, y2)
            time_efficiency_table[i][j] = distance * 1000  

    chosen_drivers = []
    total_fares = []

    if rush_hour:
        surge_multipliers = [1.5, 2.0, 1.8]
        fare_type = "Rush Hour"
    else:
        surge_multipliers = [1.0, 1.0, 1.0] 
        fare_type = "Non-Rush Hour"

    canvas.delete("all")  

    # Draw passenger nodes
    for i, (x, y) in enumerate(passenger_location):
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="black")
        canvas.create_text(x, y-20, text=f"Passenger {i+1} ({x}, {y})", fill="black")

    # Draw driver nodes
    for i, (x, y) in enumerate(driver_locations):
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue", outline="black")
        canvas.create_text(x, y+20, text=f"Driver {i+1} ({x}, {y})", fill="black")

    # Assign passengers to drivers
    assigned_edges = []
    for i in range(n):
        min_time_efficiency = float('inf')
        chosen_driver = None
        for j in range(m):
            time_efficiency = time_efficiency_table[i][j]
            if time_efficiency < min_time_efficiency:
                min_time_efficiency = time_efficiency
                chosen_driver = j

        chosen_drivers.append(chosen_driver)

        fare = calculate_fare(
            base_fare,
            calculate_distance(passenger_location[i][0], passenger_location[i][1],
                               driver_locations[chosen_driver][0], driver_locations[chosen_driver][1]),
            surge_multipliers[chosen_driver]
        )
        total_fares.append(fare)

        assigned_edges.append((passenger_location[i], driver_locations[chosen_driver]))

    # Print the efficiency table
    efficiency_text = "Efficiency Table (ms):\n"
    for row in time_efficiency_table:
        efficiency_text += ' '.join([f"{time:.2f}" for time in row]) + "\n"
    efficiency_label.config(text=efficiency_text)

    # Print the fare details
    for i, fare in enumerate(total_fares):
        result_text = f"Passenger {i+1}: Chosen Driver {chosen_drivers[i]+1} | Total Fare: ${fare:.2f}"
        result_label = ttk.Label(root, text=result_text, font=("Helvetica", 12))
        result_label.pack(pady=5)
        fare_labels.append(result_label)

    # Animate the assignment edges
    for passenger_node, driver_node in assigned_edges:
        canvas.update()
        canvas.create_line(passenger_node[0], passenger_node[1], driver_node[0], driver_node[1], fill="blue")
        canvas.after(2000)  # Delay 2 seconds

def reset_canvas():
    canvas.delete("all") 

    for label in fare_labels:
        label.pack_forget()
    fare_labels.clear()

    efficiency_label.config(text="")

root = tk.Tk()
root.title("Ride Allocation")
root.geometry("600x650")

# Styling
style = ttk.Style()
style.configure("TLabel", foreground="white", background="#263D42", padding=0, relief="solid")
style.configure("TButton", foreground="#263D42", background="#FFD166", padding=0, font=("Helvetica", 12), relief="solid")

# Canvas to draw nodes and edges
canvas = tk.Canvas(root, height=300)
canvas.pack(pady=(0, 0))

# Rush hour checkbox
rush_hour_var = tk.BooleanVar()
rush_hour_checkbox = ttk.Checkbutton(root, text="Rush Hour", variable=rush_hour_var)
rush_hour_checkbox.pack(pady=0)

# Allocate resources button
allocate_button = ttk.Button(root, text="Allocate Resources", command=allocate_resources)
allocate_button.pack(pady=(0, 0))

# Reset canvas button
reset_button = ttk.Button(root, text="Reset Canvas", command=reset_canvas)
reset_button.pack(pady=(0, 10))

# Efficiency table label
efficiency_label = ttk.Label(root, text="", font=("Courier", 10))
efficiency_label.pack(pady=(10, 5))

# List to store fare details labels
fare_labels = []

root.mainloop()
