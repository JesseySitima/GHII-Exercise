import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.connections = {}  # Dictionary to store connected nodes and their weights

    def add_edge(self, node, weight):
        self.connections[node] = weight

    def get_edges(self):
        return self.connections.keys()

class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes in the graph

    def add_node(self, name):
        node = Node(name)
        self.nodes[name] = node

    def add_edge(self, node1_name, node2_name, weight):
        if node1_name in self.nodes and node2_name in self.nodes:
            node1 = self.nodes[node1_name]
            node2 = self.nodes[node2_name]
            node1.add_edge(node2, weight)
            node2.add_edge(node1, weight)
        else:
            print("Node not found in the graph.")

    def get_node(self, name):
        return self.nodes.get(name, None)

    def convert_to_networkx(self):
        # Create a NetworkX graph and add nodes and edges
        G = nx.Graph()
        for node_name, node in self.nodes.items():
            G.add_node(node_name)
            for neighbor, weight in node.connections.items():
                G.add_edge(node_name, neighbor.name, weight=weight)
        return G

    def shortest_path(self, start_district, end_district):
        # Convert your custom graph to a NetworkX graph
        nx_graph = self.convert_to_networkx()

        try:
            # Use NetworkX's built-in shortest path function
            shortest_path = nx.shortest_path(nx_graph, source=start_district, target=end_district, weight='weight')
            shortest_path_length = nx.shortest_path_length(nx_graph, source=start_district, target=end_district, weight='weight')
            
            return shortest_path, shortest_path_length
        except nx.NetworkXNoPath:
            return None, float('inf')

    def __str__(self):
        graph_str = ""
        for node_name, node in self.nodes.items():
            connections = ", ".join([f"{neighbor.name}({weight})" for neighbor, weight in node.connections.items()])
            graph_str += f"{node_name} -> {connections}\n"
        return graph_str

# Graph object
my_graph = Graph()

# Adding nodes to the graph
districts = ['Mchinji', 'Kasungu', 'Lilongwe', 'Dowa', 'Ntchisi', 'Nkhotakota', 'Salima', 'Dedza', 'Ntcheu']
for district in districts:
    my_graph.add_node(district)

# Adding edges with weights
edges = [('Mchinji', 'Kasungu', 141), ('Mchinji', 'Lilongwe', 109), ('Kasungu', 'Ntchisi', 66), ('Kasungu', 'Dowa', 117),
         ('Lilongwe', 'Dowa', 55), ('Lilongwe', 'Dedza', 92), ('Dowa', 'Ntchisi', 38), ('Dowa', 'Salima', 67),
         ('Ntchisi', 'Nkhotakota', 66), ('Nkhotakota', 'Salima', 112), ('Salima', 'Dedza', 96), ('Dedza', 'Ntcheu', 74)]

for u, v, weight in edges:
    my_graph.add_edge(u, v, weight)

# Function to find the shortest path between any two districts
def find_shortest_path(graph, start_district, end_district):
    return graph.shortest_path(start_district, end_district)

# Display the results for all pairs of districts
for start_district in districts:
    for end_district in districts:
        if start_district != end_district:
            path, length = find_shortest_path(my_graph, start_district, end_district)
            if path:
                print(f"Shortest path from {start_district} to {end_district}: {path}")
                print(f"Shortest path length: {length}")
            else:
                print(f"No path found from {start_district} to {end_district}.")


# Create a NetworkX graph from the custom graph
G = nx.Graph()

for node_name, node in my_graph.nodes.items():
    for neighbor, weight in node.connections.items():
        G.add_edge(node_name, neighbor.name, weight=weight)

# Draw the graph using NetworkX and Matplotlib
pos = nx.spring_layout(G, seed=42)  # You can use different layout algorithms
labels = {node: node for node in G.nodes()}
edge_labels = {(u, v): w['weight'] for u, v, w in G.edges(data=True)}

nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color='lightblue', font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.show()