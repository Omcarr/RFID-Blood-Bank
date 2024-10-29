import heapq

# Define a class for the Blood Bank
class BloodBank:
    def __init__(self, name, blood_types, connections):
        self.name = name
        self.blood_types = blood_types 
        self.connections = connections 

# Function to find the shortest path to a blood bank with the required blood type
def find_nearest_blood_bank(start, blood_type, graph):
    # Priority queue to store (distance, blood bank)
    priority_queue = [(0, start)]
    # Dictionary to store the shortest distances
    distances = {bank.name: float('inf') for bank in graph}
    distances[start.name] = 0
    # To track the path
    previous_nodes = {bank.name: None for bank in graph}

    while priority_queue:
        current_distance, current_bank = heapq.heappop(priority_queue)

        # Check if the blood bank has the required blood type
        if blood_type in current_bank.blood_types:
            # Retrieve the path
            path = []
            while current_bank is not None:
                path.append(current_bank.name)
                current_bank = previous_nodes[current_bank.name]
            path.reverse()
            return current_distance, path

        for neighbor_name, distance in current_bank.connections.items():
            neighbor = next(bank for bank in graph if bank.name == neighbor_name)
            new_distance = current_distance + distance

            # If a shorter path is found
            if new_distance < distances[neighbor.name]:
                distances[neighbor.name] = new_distance
                previous_nodes[neighbor.name] = current_bank
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # If no suitable blood bank is found
    return float('inf'), []
