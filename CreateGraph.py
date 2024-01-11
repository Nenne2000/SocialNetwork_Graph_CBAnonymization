import pandas as pd
import networkx as nx
import numpy as np
from faker import Faker
import matplotlib.pyplot as plt

#Creazione del grafo bipartito
#valori di n ed m scelti dall'utente
n = int(input("Inserisci il numero di nodi di tipo User: "))
m = int(input("Inserisci il numero di nodi di tipo Interaction: "))
k = int(input("Inserisci il numero di archi: "))
G = nx.bipartite.gnmk_random_graph(n, m, k)



#creiamo i due insiemi che useremo per semplificare i richiami successivi
nodes_0 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 0]
nodes_1 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 1]

#Aggiungimao valori fittizi circa i dati relativi agli utenti
fake = Faker()
for node in nodes_0:
    G.nodes[node]["ID"] = node
    G.nodes[node]["name"] = "".join(fake.name())
    G.nodes[node]["year"] = np.random.randint(1940, 2000)
    G.nodes[node]["color"] = "green"

#Diamo un valore fittizio anche ai nodi interazione, includendo nel nostro dominio interazioni di tipo friendship, blog e message
for node in nodes_1:
    G.nodes[node]["ID"] = node
    G.nodes[node]["interaction"] = np.random.choice(["friendship", "blog", "message"])
    G.nodes[node]["color"] = "blue"


# Correzioni necessarie circa il numero di archi per ogni nodo di tipo interazione
for node in nodes_1:
    neighbors = list(G.neighbors(node))
    #se per ogni interazione è stato generato un solo vicino, lo rimuoviamo, poiche non avrebbe senso
    if len(neighbors) == 1:
        G.remove_edge(node, neighbors[0])
    #Il numero massimo di utenti connessi tramite amicizia o messaggio è 2, il numero massimo di utenti connessi tramite blog è 4
    if (G.nodes[node]["interaction"] == "friendship" or G.nodes[node]["interaction"] == "message") and len(neighbors) > 2:
        G.remove_edges_from([(node, neighbor) for neighbor in neighbors[2:]])
    elif G.nodes[node]["interaction"] == "blog" and len(neighbors) > 4:
        G.remove_edges_from([(node, neighbor) for neighbor in neighbors[4:]])

#stampiamo i valori generati per ogni attributo dei nodi
for node in nodes_0:
    print(f"Node {node}: ID = {G.nodes[node]['ID']}, name = {G.nodes[node]['name']}, year = {G.nodes[node]['year']}, type = User")
for node in nodes_1:
    print(f"Node {node}: ID = {G.nodes[node]['ID']}, interaction = {G.nodes[node]['interaction']}, type = Interaction")

# Creazione di un DataFrame da nodi e archi del grafo
nodes_data = [(node, G.nodes[node]) for node in G.nodes()]
edges_data = [(edge[0], edge[1], G[edge[0]][edge[1]]) for edge in G.edges()]

nodes_df = pd.DataFrame(nodes_data, columns=["node", "attributes"])
edges_df = pd.DataFrame(edges_data, columns=["node1", "node2", "attributes"])

# Salvataggio del DataFrame in file CSV
nodes_df.to_csv("nodes_data.csv", index=False)
edges_df.to_csv("edges_data.csv", index=False)

# Visualizzazione del grafo
pos_loaded = nx.bipartite_layout(G, nodes_0)
nx.draw(G, pos_loaded, with_labels=False, node_color=[G.nodes[node]["color"] for node in G.nodes()], verticalalignment="bottom")
nx.draw_networkx_labels(G, pos_loaded, {node: G.nodes[node]["interaction"] for node in G.nodes() if G.nodes[node]["bipartite"] == 1}, font_size=10, font_color="black", verticalalignment="center")
nx.draw_networkx_labels(G, pos_loaded, {node: node for node in G.nodes() if G.nodes[node]["bipartite"] == 0}, font_size=10, font_color="black", verticalalignment="center")
plt.show()