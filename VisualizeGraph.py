import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Carica i dati dai file CSV
nodes_df = pd.read_csv("nodes_data.csv")
edges_df = pd.read_csv("edges_data.csv")

# Crea un grafo vuoto
G_loaded = nx.Graph()

# Aggiungi nodi e attributi dal DataFrame dei nodi
for _, data in nodes_df.iterrows():
    G_loaded.add_node(data["node"], **eval(data["attributes"]))

# Aggiungi archi e attributi dal DataFrame degli archi
for _, data in edges_df.iterrows():
    G_loaded.add_edge(data["node1"], data["node2"], **eval(data["attributes"]))

# Divide nuovamente il grafo in due tipi
nodes_0_loaded = [node for node in G_loaded.nodes() if G_loaded.nodes[node]["bipartite"] == 0]
nodes_1_loaded = [node for node in G_loaded.nodes() if G_loaded.nodes[node]["bipartite"] == 1]

# Visualizza il grafo caricato
pos_loaded = nx.bipartite_layout(G_loaded, nodes_0_loaded)
nx.draw(G_loaded, pos_loaded, with_labels=False, node_color=[G_loaded.nodes[node]["color"] for node in G_loaded.nodes()], verticalalignment="bottom")
nx.draw_networkx_labels(G_loaded, pos_loaded, {node: G_loaded.nodes[node]["interaction"] for node in G_loaded.nodes() if G_loaded.nodes[node]["type"] == 1}, font_size=10, font_color="black", verticalalignment="center")
nx.draw_networkx_labels(G_loaded, pos_loaded, {node: node for node in G_loaded.nodes() if G_loaded.nodes[node]["type"] == 0}, font_size=10, font_color="black", verticalalignment="center")
plt.show()