import os
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from faker import Faker

##############################################################################################################################################################################

#Creazione del grafo bipartito
n = 30
m = 20
k = n*2
G = nx.bipartite.gnmk_random_graph(n, m, k)

#Divisione esplicita dei 2 tipi di dato
for node in range(n):
    G.nodes[node]["type"] = 0

for node in range(n, n+m):
    G.nodes[node]["type"] = 1

#creiamo i due insiemi che useremo per semplificare i richiami successivi
nodes_0 = [node for node in G.nodes() if G.nodes[node]["type"] == 0]
nodes_1 = [node for node in G.nodes() if G.nodes[node]["type"] == 1]

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

##############################################################################################################################################################################

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

##############################################################################################################################################################################
'''
#stampiamo i valori degli attributi utili per la comprensione
for node in nodes_0:
    print(f"Node {node}: ID = {G.nodes[node]['ID']}, name = {G.nodes[node]['name']}, year = {G.nodes[node]['year']}")
for node in nodes_1:
    print(f"Node {node}: ID = {G.nodes[node]['ID']}, interaction = {G.nodes[node]['interaction']}")
'''
##############################################################################################################################################################################

#funzioni necessarie Per la divisione in classi + creazione delle label lists

#Ordiniamo i nodi di tipo 0 rispetto al valore dell'attributo year, perché in base al contesto poniamo che gli utenti di età simile abbiano più probabilità di essere amici, avere blog condivisi e inviarsi messaggi
def sort(V):
    V.sort(key=lambda x: G.nodes[x]["year"], reverse=True)
    return V

# verifica che il nodo v non abbia già interazioni con nodi della classe c   
def safety_condition(c, v):
    for node_in_class in c:
        # Verifica se hanno almeno un nodo in comune
        if set(G.neighbors(node_in_class)).intersection(set(G.neighbors(v))):
            return False
    return True

#per ogni elemento di una classe creiamo una label list che maschera l'identificatore dell'utente in base ad un pattern di lunghezza k < m  del tipo [0,1,2,...,k-1] (prefix pattern)
def create_lbl_list_prefix_pattern(node_pos, c):
    pattern = [0,1,2]
    k = len(pattern)
    lbl_list_pos = []
    for i in pattern:
        lbl_list_pos.append((node_pos + i) % len(c))
    lbl_list = []
    for i in lbl_list_pos:
        lbl_list.append(c[i])
    np.random.shuffle(lbl_list)
    return lbl_list

##############################################################################################################################################################################

V = nodes_0  #V è un rename per la lista degli utenti
class_size = 5   #size massima della classe
classes = []
sort(V)
for v in V:
    flag = True
    #finché non troviamo una classe che rispetta la safety condition o che non ha raggiunto la size massima
    for c in classes:
        if safety_condition(c, v) and len(c) < class_size:
            c.append(v)
            flag = False
            break
    if flag:
        new_class = []
        new_class.append(v)
        classes.append(new_class)

for node in nodes_0:
    for c in classes:
        if node in c:
            G.nodes[node]["set"] = c

for c in classes:
    print(c)

##############################################################################################################################################################################
    
#Implementazione del partitioning approach, dove ogni classe creata precedentemente diventerà un "ipernodo" di un nuovo grafo, che rimane bipartito
#Ogni nodo appartentente al precedente grafo permette di mantenere gli archi in cui è coinvolto
    
#creo il nuovo grafo bipartito dove n2 è il numero di classi e m è nuovamente il numero di interazioni (rimasto invariato)
n2 = len(classes)
G_partitioned = nx.Graph()

#aggiungo come nodi di tipo bipartite=0 gli array che corrispondono alle classi
for i in range(n2):
    G_partitioned.add_node("P"+str(i), bipartite=0)

#ora da n2 ad m aggiungiamo le interactions, come nel caso precedente
for i in range(n2, n2+m):
    corrispondent_node = nodes_1[i-n2]
    G_partitioned.add_node(corrispondent_node, bipartite=1)
    
nodes_0_partitioned = [node for node in G_partitioned.nodes() if G_partitioned.nodes[node]["bipartite"] == 0]
nodes_1_partitioned = [node for node in G_partitioned.nodes() if G_partitioned.nodes[node]["bipartite"] == 1]

for i, node in enumerate(nodes_0_partitioned):
    G_partitioned.nodes[node]["ID"] = node
    G_partitioned.nodes[node]["color"] = "green"
    G_partitioned.nodes[node]["set"] = classes[i]
    print(G_partitioned.nodes[node]["set"])

for i, node in enumerate(nodes_1_partitioned):
    G_partitioned.nodes[node]["ID"] = i+n
    G_partitioned.nodes[node]["interaction"] = G.nodes[i+n]["interaction"]
    G_partitioned.nodes[node]["color"] = "blue"

for edge in G.edges():
    for node in nodes_0_partitioned:
        if edge[0] in G_partitioned.nodes[node]["set"]:
            G_partitioned.add_edge(node, edge[1])


##############################################################################################################################################################################
'''
#creiamo e stampiamo le le label lists create tramite il prefix pattern
for c in classes:
    lista_di_liste = []
    for node_pos in range(len(c)):
        lista_di_liste.append(create_lbl_list_prefix_pattern(node_pos, c))
    print(lista_di_liste)
'''
# rappresentazione del grafo originale bipartito
pos = nx.bipartite_layout(G, nodes_0)
nx.draw(G, pos, with_labels=False, node_color=[G.nodes[node]["color"] for node in G.nodes()], verticalalignment="bottom")
nx.draw_networkx_labels(G, pos, {node: G.nodes[node]["interaction"] for node in G.nodes() if G.nodes[node]["bipartite"] == 1}, font_size=10, font_color="black", verticalalignment="center")
nx.draw_networkx_labels(G, pos, {node: node for node in G.nodes() if G.nodes[node]["bipartite"] == 0}, font_size=10, font_color="black", verticalalignment="center")
plt.show()

#stampa del grafo originale ma le label lists rimpiazzano gli ID degli utenti
pos = nx.bipartite_layout(G, nodes_0)
nx.draw(G, pos, with_labels=False, node_color=[G.nodes[node]["color"] for node in G.nodes()], verticalalignment="bottom")
nx.draw_networkx_labels(G, pos, {node: G.nodes[node]["interaction"] for node in G.nodes() if G.nodes[node]["bipartite"] == 1}, font_size=10, font_color="black", verticalalignment="center")
nx.draw_networkx_labels(G, pos, {node: G.nodes[node]["set"] for node in G.nodes() if G.nodes[node]["bipartite"] == 0}, font_size=10, font_color="black", verticalalignment="center")
plt.show()

#stampa del grafo partitioned
pos = nx.bipartite_layout(G_partitioned, nodes_0_partitioned)
nx.draw(G_partitioned, pos, with_labels=False, node_color=[G_partitioned.nodes[node]["color"] for node in G_partitioned.nodes()], verticalalignment="bottom")
nx.draw_networkx_labels(G_partitioned, pos, {node: G_partitioned.nodes[node]["interaction"] for node in G_partitioned.nodes() if G_partitioned.nodes[node]["bipartite"] == 1}, font_size=10, font_color="black", verticalalignment="center")
nx.draw_networkx_labels(G_partitioned, pos, {node: node for node in G_partitioned.nodes() if G_partitioned.nodes[node]["bipartite"] == 0}, font_size=10, font_color="black", verticalalignment="center")
plt.show()
