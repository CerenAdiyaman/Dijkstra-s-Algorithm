import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pandas as pd



def dijkstra_algorithm(G, source):
    # Initialize distances, previous nodes, and visited nodes
    distances = {node: float('inf') for node in G.nodes()}
    distances[source] = 0
    previous_nodes = {node: None for node in G.nodes()}
    visited = []  # Tracks fully processed nodes
    steps_data = []  # Collects data for table visualization

    unvisited = list(G.nodes())  # List of all unvisited nodes
    current = source  # Start from the source node

    while unvisited:  # While there are unvisited nodes
        # Update distances for each neighbor of the current node
        for neighbor in G.neighbors(current):
            if neighbor in unvisited:
                new_distance = distances[current] + G[current][neighbor]["weight"]
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current

        # Mark the current node as visited
        visited.append(current)
        unvisited.remove(current)  # Remove the current node from unvisited list

        # Choose the unvisited node with the smallest distance
        if unvisited:
            current = min(unvisited, key=lambda node: distances[node])

        # Record step data for visualization
        steps_data.append({
            'Node': list(distances.keys()),
            'Previous': [previous_nodes[n] for n in distances.keys()],
            'Distance': [distances[n] for n in distances.keys()],
            'Visited': ['Yes' if n in visited else 'No' for n in distances.keys()]
        })

    return distances, previous_nodes, visited, steps_data

graph_type = input("Choose graph type (directed/undirected): ").strip().lower()
if graph_type == "directed":
    G = nx.DiGraph()
elif graph_type == "undirected":
    G = nx.Graph()
else:
    raise ValueError("Unvalid. 'directed' or 'undirected'.")

G.add_weighted_edges_from([
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("D", "E", 2),
    ("F", "D", 4)
])

# Define source node
source = "A"
distances, previous_nodes, visited, steps_data = dijkstra_algorithm(G, source)

# Visualization 
pos = nx.spring_layout(G)
fig, (ax_graph, ax_table) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [2, 1]})

frame_num = 0  
animation_paused = False

def update(num):
    ax_graph.clear()
    ax_table.clear()

    # Draw the graph
    nx.draw_networkx_edges(G, pos, ax=ax_graph, edge_color="gray", width=1)
    
    # Highlight edges of the current node in orange
    if num < len(visited):
        current_node = visited[num]
        current_edges = [(current_node, neighbor) for neighbor in G.neighbors(current_node)]
        nx.draw_networkx_edges(G, pos, edgelist=current_edges, ax=ax_graph, edge_color="orange", width=2)

    # Node colors: visited nodes are red, others are blue
    visited_nodes = visited[:num + 1]
    node_colors = ['lightcoral' if node in visited_nodes else 'lightblue' for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, ax=ax_graph, node_size=500, node_color=node_colors)
    nx.draw_networkx_labels(G, pos, ax=ax_graph)

    # Add weights to edges
    nx.draw_networkx_edge_labels(G, pos, ax=ax_graph, edge_labels={(u, v): G[u][v]["weight"] for u, v in G.edges()})

    ax_graph.set_title(f"Dijkstra Algorithm - Step {num + 1}")

    # Display the table for distances, previous nodes, and visited status
    step_data = steps_data[min(num, len(steps_data)-1)]
    df = pd.DataFrame(step_data)
    ax_table.axis('off')

    table = ax_table.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(0.8, 0.8)

    plt.pause(10)  # Synchronize the update of graph and table with a pause

def play(event):
    global animation_paused
    animation_paused = False

def pause(event):
    global animation_paused
    animation_paused = True

def restart(event):
    global frame_num, animation_paused
    frame_num = 0
    animation_paused = False
    update(frame_num)
    plt.draw()
    animate()

def close_window(event):
    plt.close()

def animate():
    global frame_num, animation_paused
    while frame_num < len(visited):
        if not animation_paused:
            update(frame_num)
            frame_num += 1
        else:
            plt.pause(1)


# Highlight the shortest path in green after algorithm completes
def highlight_shortest_paths():
    nx.draw_networkx_edges(G, pos, ax=ax_graph, edge_color="gray", width=1)

    shortest_paths = []
    for target in G.nodes():
        path = []
        node = target
        while node is not None:
            path.append(node)
            node = previous_nodes[node]
        path.reverse()
        for i in range(len(path) - 1):
            shortest_paths.append((path[i], path[i + 1]))
    
    # Highlight shortest paths in green
    nx.draw_networkx_edges(G, pos, edgelist=shortest_paths, ax=ax_graph, edge_color="green", width=2)

# Add control buttons
ax_play = plt.axes([0.26, 0.02, 0.1, 0.05])
btn_play = Button(ax_play, 'Play')
btn_play.on_clicked(play)

ax_pause = plt.axes([0.38, 0.02, 0.1, 0.05])
btn_pause = Button(ax_pause, 'Pause')
btn_pause.on_clicked(pause)

ax_restart = plt.axes([0.50, 0.02, 0.1, 0.05])
btn_restart = Button(ax_restart, 'Restart')
btn_restart.on_clicked(restart)

ax_close = plt.axes([0.62, 0.02, 0.1, 0.05])
btn_close = Button(ax_close, 'Close')
btn_close.on_clicked(close_window)

animate()
highlight_shortest_paths()

plt.tight_layout()
plt.show()