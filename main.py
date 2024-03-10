import pandas as pd
import networkx as nx
import scipy as sp
import matplotlib.pyplot as plt
import random


def display_grid(list_of_lists, num_lists_per_row):
    for i in range(0, len(list_of_lists), num_lists_per_row):
        row = list_of_lists[i:i+num_lists_per_row]
        print(row)


def plot(count):
    pos = {(i, j): (j, -i) for i in range(num_rows) for j in range(num_cols)}
    ax = plt.figure().gca()
    ax.set_axis_off()
    node_colors = [G.nodes[n]['color'] for n in G.nodes()]
    nx.draw_networkx(G, pos, with_labels=False, node_color=node_colors, node_size=20)
    plt.savefig(f"/Users/sroche/PycharmProjects/pythonProject1/imgs/{count}.png", dpi=150)
    plt.close()
    # plt.show()


df = pd.read_csv('/Users/sroche/Downloads/EMAG2_V3_20170530.zip', compression='zip')

df = df[df.iloc[:, 2].between(253.773193, 255.053101)]
df = df[df.iloc[:, 3].between(39.554883, 40.547200)]

longitude_values = df.iloc[:, 2].to_list()
latitude_values = df.iloc[:, 3].to_list()
mag_values_point = df.iloc[:, 5].tolist()
mag_values = []
for val in mag_values_point:
    if val >= 0:
        mag_values.append([float("{:.3f}".format(val - 0.05 * val)), float("{:.3f}".format(val + 0.05 * val))])
    else:
        mag_values.append([float("{:.3f}".format(val + 0.05 * val)), float("{:.3f}".format(val - 0.05 * val))])

# num_elements_per_row = 39  # Number of elements per row
#
# # Display the grid
# display_grid(mag_values, num_elements_per_row)

G = nx.Graph()

num_rows = 29
num_cols = 39
# Add nodes
count = 0
for i in range(num_rows):
    for j in range(num_cols):
        G.add_node((i, j), nT=mag_values[j + i * num_rows], color="red")

# Add edges (connecting adjacent nodes)
for i in range(num_rows):
    for j in range(num_cols):
        if i < num_rows - 1:
            G.add_edge((i, j), (i + 1, j))
        if j < num_cols - 1:
            G.add_edge((i, j), (i, j + 1))
        # Connect to the upper-left corner
        if i > 0 and j > 0:
            G.add_edge((i, j), (i - 1, j - 1))
        # Connect to the upper-right corner
        if i > 0 and j < num_cols - 1:
            G.add_edge((i, j), (i - 1, j + 1))
        # Connect to the lower-left corner
        if i < num_rows - 1 and j > 0:
            G.add_edge((i, j), (i + 1, j - 1))
        # Connect to the lower-right corner
        if i < num_rows - 1 and j < num_cols - 1:
            G.add_edge((i, j), (i + 1, j + 1))

# set up
# initial_spot = [20, 20]
initial_val = G.nodes[20, 20]['nT']
path_nodes = [G.nodes[15, 1], G.nodes[15, 2], G.nodes[15, 3], G.nodes[15, 4], G.nodes[15, 5],
              G.nodes[15, 6], G.nodes[15, 7], G.nodes[15, 8], G.nodes[15, 9], G.nodes[15, 10],
              G.nodes[15, 11], G.nodes[15, 12], G.nodes[15, 13], G.nodes[15, 14], G.nodes[15, 15],
              G.nodes[15, 16], G.nodes[15, 17], G.nodes[15, 18], G.nodes[15, 19], G.nodes[15, 20],
              G.nodes[15, 21], G.nodes[15, 22], G.nodes[15, 23], G.nodes[15, 24], G.nodes[15, 25],
              G.nodes[15, 26], G.nodes[15, 27], G.nodes[15, 28], G.nodes[15, 29], G.nodes[15, 30],
              G.nodes[15, 31], G.nodes[15, 32], G.nodes[15, 33], G.nodes[15, 34], G.nodes[15, 35]]

path_vals = []
for node in path_nodes:
    val = node['nT']
    path_vals.append(val)

for node in path_nodes:
    node['color'] = 'yellow'

plot("path")
for node in path_nodes:
    node['color'] = 'red'

path_nodes[0]['color'] = 'blue'
plot("start")

input_vals = []
curr_nodes = [[15, 1]]
for interval in path_vals:
    input_vals.append(random.uniform(interval[0], interval[1]))

for count, in_val in enumerate(input_vals[1:]):
    new_list = []
    for node in curr_nodes:
        # Get neighbors of the current node
        neighbors = list(G.neighbors((node[0], node[1])))
        enlarged_neighbors = []
        for neighbor in neighbors:
            enlarged_neighbors.extend(list(G.neighbors(neighbor)))
        enlarged_set = set(enlarged_neighbors)
        for neighbor in list(enlarged_set):
            # Assuming neighbor is a node identifier (hashable type)
            if G.nodes[neighbor[0], neighbor[1]]['nT'][0] <= in_val <= G.nodes[neighbor[0], neighbor[1]]['nT'][1]:
                new_list.append([neighbor[0], neighbor[1]])
                G.nodes[neighbor[0], neighbor[1]]['color'] = 'blue'
        G.nodes[node[0], node[1]]['color'] = 'red'
    plot(count)
    curr_nodes = new_list

# Call the plot function to visualize the updated graph
plot(len(input_vals[1:]) + 1)
