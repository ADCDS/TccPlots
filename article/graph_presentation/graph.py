import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from(
    [('B', 'A'), ('A', 'C'), ('B', 'D'), ('E', 'F'),
     ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G'), ('A', 'C'), ('C', 'E')])


# Specify the edges you want here
red_edges = []
colors = ['red','cyan','yellow','cyan','green','cyan','cyan','cyan']
edge_colours = ['black' if not edge in red_edges else 'red'
                for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.circular_layout(G)
pos['A'] = [1, 2]
pos['D'] = [1.5, 0.7]
pos['C'] = [0, 1.99]
pos['G'] = [0, 0.99]
nx.draw_networkx_nodes(G, pos, node_size=500, node_color=colors)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
plt.show()
