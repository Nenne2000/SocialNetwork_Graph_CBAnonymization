import os
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from faker import Faker

##############################################################################################################################################################################

# Creazione del grafo bipartito con nodi di tipo 0 e nodi di tipo 1
n = 15
m = 8
p = 0.5
k = int(p * n * m)
G = nx.bipartite.gnmk_random_graph(n, m, k)

#per ogni nodo di tipo 0, assegna un attributo "type" con valore 0
for node in range(n):
    G.nodes[node]["type"] = 0

#per ogni nodo di tipo 1, assegna un attributo "type" con valore 1
for node in range(n, n+m):
    G.nodes[node]["type"] = 1

#prendi tutti i nodi con type = 0 e crea un insieme
nodes_0 = [node for node in G.nodes() if G.nodes[node]["type"] == 0]
#prendi tutti i nodi con type = 1 e crea un insieme
nodes_1 = [node for node in G.nodes() if G.nodes[node]["type"] == 1]

fake = Faker()
#dobbiamo dare ad ogni nodo di tipo 0 un attributo "name" ed un attributo "year" con come valore un numero intero casuale tra 1940 e 2000
for node in nodes_0:
    G.nodes[node]["ID"] = node
    G.nodes[node]["name"] = "".join(fake.name())
    G.nodes[node]["year"] = np.random.randint(1940, 2000)
    G.nodes[node]["color"] = "green"

#dobbiamo dare ad ogni nodo di tipo 1 un attributo "interaction" con valore casuale tra "like", "friendship", "blog", "message"
for node in nodes_1:
    G.nodes[node]["ID"] = node
    G.nodes[node]["interaction"] = np.random.choice(["friendship", "blog", "message"])
    G.nodes[node]["color"] = "blue"

##############################################################################################################################################################################

# Limitazione del numero di archi per ogni nodo del secondo gruppo
for node in nodes_1:
    neighbors = list(G.neighbors(node))
    if G.nodes[node]["interaction"] == "friendship":
        if len(neighbors) > 2:
            G.remove_edges_from([(node, neighbor) for neighbor in neighbors[2:]])
    elif G.nodes[node]["interaction"] == "message":
        if len(neighbors) > 3:
            G.remove_edges_from([(node, neighbor) for neighbor in neighbors[2:]])
    elif G.nodes[node]["interaction"] == "blog":
        if len(neighbors) > 4:
            G.remove_edges_from([(node, neighbor) for neighbor in neighbors[4:]])

#stampiamo i valori degli attributi name e year dei nodi di tipo 0
for node in nodes_0:
    print(f"Node {node}: ID = {G.nodes[node]['ID']}, name = {G.nodes[node]['name']}, year = {G.nodes[node]['year']}")

#stampiamo i valori degli attributi interaction dei nodi di tipo 1
for node in nodes_1:
    print(f"Node {node}: ID = {G.nodes[node]['ID']}, interaction = {G.nodes[node]['interaction']}")

pos = nx.bipartite_layout(G, nodes_0)
nx.draw(G, pos, with_labels=False, node_color=[G.nodes[node]["color"] for node in G.nodes()], verticalalignment="bottom")
nx.draw_networkx_labels(G, pos, {node: G.nodes[node]["interaction"] for node in G.nodes() if G.nodes[node]["bipartite"] == 1}, font_size=10, font_color="black", verticalalignment="center")
nx.draw_networkx_labels(G, pos, {node: node for node in G.nodes() if G.nodes[node]["bipartite"] == 0}, font_size=10, font_color="black", verticalalignment="center")
plt.show()

#salviamo il grafo in un file .csv
nx.write_gexf(G, "csv/graph.gexf")