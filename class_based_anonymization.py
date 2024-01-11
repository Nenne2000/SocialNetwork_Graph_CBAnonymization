import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# Carica i dati dai file CSV
nodes_df = pd.read_csv("nodes_data.csv")
edges_df = pd.read_csv("edges_data.csv")

# Crea un grafo vuoto
G = nx.Graph()

# Aggiungi nodi e attributi dal DataFrame dei nodi
for _, data in nodes_df.iterrows():
    G.add_node(data["node"], **eval(data["attributes"]))

# Aggiungi archi e attributi dal DataFrame degli archi
for _, data in edges_df.iterrows():
    G.add_edge(data["node1"], data["node2"], **eval(data["attributes"]))

# Divide nuovamente il grafo in due tipi
nodes_0 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 0]
nodes_1 = [node for node in G.nodes() if G.nodes[node]["bipartite"] == 1]

n = len(nodes_0)
m = len(nodes_1)
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

for i, node in enumerate(nodes_1_partitioned):
    G_partitioned.nodes[node]["ID"] = i+n
    G_partitioned.nodes[node]["interaction"] = G.nodes[i+n]["interaction"]
    G_partitioned.nodes[node]["color"] = "blue"

for edge in G.edges():
    for node in nodes_0_partitioned:
        if edge[0] in G_partitioned.nodes[node]["set"]:
            G_partitioned.add_edge(node, edge[1])

##############################################################################################################################################################################

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
