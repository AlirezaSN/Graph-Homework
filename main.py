###################################### imports ######################################

import collections
import networkx as nx
import matplotlib.pyplot as plt

###################################### Code ######################################

################### dataset files ###################

FACEBOOK_DATASET = 'datasets/facebook_combined.txt'
CA_ASTRO_PH = 'datasets/CA-AstroPh.txt'
EMAIL_DATASET = 'datasets/Email-Enron.txt'

######################################

graph = nx.read_edgelist(FACEBOOK_DATASET, create_using=nx.Graph(), nodetype=int)

################### Number of Nodes ###################

def get_number_of_nodes():
    number_of_nodes = graph.number_of_nodes()
    print('number of nodes: ', number_of_nodes)

################### Number of Edges ###################

def get_number_of_edges():
    number_of_edges = graph.number_of_edges()
    print('number of edges: ', number_of_edges)

################### Average Degree ###################

def get_average_degree():
    total_degrees = 0
    for d in graph.degree():
        total_degrees += d[1]
    average_degree = total_degrees / number_of_nodes
    print('average degree: ', average_degree)

################### Density ###################

def get_density():
    density = nx.density(graph)
    print('density: ', density)

################### Clustering Coefficient 1 ###################

def get_first_cc():
    transitivity = nx.transitivity(graph)
    print('clustering coefficient 1 (transivity): ', transitivity)

################### Clustering Coefficient 2 ###################

def get_second_cc():
    average_clustering = nx.average_clustering(graph)
    print('clustering coefficient 2: ', average_clustering)

################### Diameter ###################

def get_diameter():
    diamter = nx.diameter(graph)
    print('diameter: ', diamter)

################### Average Shortest Path Length ###################

def get_average_shortest_path():
    average_shortest_path = nx.average_shortest_path_length(graph)
    print('average shortest path: ', average_shortest_path)

################### Degree Distribution Plot ###################

def draw_degree_distribution():
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = sorted(nx.connected_component_subgraphs(graph), key=len, reverse=True)[0]
    pos = nx.spring_layout(graph)
    plt.axis('off')
    nx.draw_networkx_nodes(graph, pos, node_size=20)
    nx.draw_networkx_edges(graph, pos, alpha=0.4)

    plt.show()

################### Assortivity ###################

def get_assortivity():
    degree_assortativity_coefficient = nx.degree_assortativity_coefficient(graph)
    print('degree assortativity coefficient: ', "%3.1f"%degree_assortativity_coefficient)

################### Centrality 1: ###################

def get_degree_centrality():
    degree_centrality = nx.degree_centrality(graph)
    print('top 5 at degree centrality: ', degree_centrality)

################### Centrality 2: ###################

def get_closeness_centrality():
    closeness_centrality = nx.closeness_centrality(graph)
    print('top 5 at closeness centrality: ', closeness_centrality)

################### Centrality 3: ###################

def get_betweenness_centrality():
    betweenness_centrality = nx.betweenness_centrality(graph)
    print('top 5 at betweenness centrality: ', betweenness_centrality)

################### Network Centralization ###################

def get_centralization():
    pass

###################################### Excecution ######################################

if __name__ == '__main__':
    get_number_of_nodes()
    get_number_of_edges()
    get_average_degree()
    get_density()
    get_first_cc()
    et_second_cc()
    get_diameter()
    get_average_shortest_path()
    get_assortivity()
    get_degree_centrality()
    get_closeness_centrality()
    get_betweenness_centrality()
    get_centralization()
    #draw_degree_distribution()