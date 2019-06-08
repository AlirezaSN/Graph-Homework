###################################### imports ######################################

import sys
import os.path
import random
import collections
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics.SIRModel as sir
import ndlib.models.epidemics.SIModel as si
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend
from ndlib.viz.bokeh.DiffusionPrevalence import DiffusionPrevalence
from ndlib.viz.bokeh.MultiPlot import MultiPlot

###################################### Code ######################################

################### dataset files ###################

DATASET_FOLDER = 'datasets/'

################### Number of Nodes ###################

def get_number_of_nodes(graph):
    number_of_nodes = graph.number_of_nodes()
    print('number of nodes: ', number_of_nodes)

################### Number of Edges ###################

def get_number_of_edges(graph):
    number_of_edges = graph.number_of_edges()
    print('number of edges: ', number_of_edges)

################### Average Degree ###################

def get_average_degree(graph):
    total_degrees = 0
    for d in graph.degree():
        total_degrees += d[1]
    average_degree = total_degrees / graph.number_of_nodes()
    print('average degree: ', average_degree)

################### Density ###################

def get_density(graph):
    density = nx.density(graph)
    print('density: ', density)

################### Clustering Coefficient 1 ###################

def get_first_cc(graph):
    transitivity = nx.transitivity(graph)
    print('clustering coefficient 1 (transivity): ', transitivity)

################### Clustering Coefficient 2 ###################

def get_second_cc(graph):
    average_clustering = nx.average_clustering(graph)
    print('clustering coefficient 2: ', average_clustering)

################### Diameter ###################

def get_diameter(graph):
    if nx.is_connected(graph):
        diamter = nx.diameter(graph)
        print('diameter: ', diamter)
    else:
        components = nx.connected_components(graph)
        number_connected_components = nx.number_connected_components(graph)
        print('graph is disconnected ... number of components are: ', number_connected_components)
        diameter = 0
        for component in components:
            subgraph = graph.subgraph(component)
            sub_diameter = nx.diameter(subgraph)
            if sub_diameter > diameter:
                diameter = sub_diameter
        print('diameter: ', diameter)

################### Average Shortest Path Length ###################

def get_average_shortest_path(graph):
    if nx.is_connected(graph):
        average_shortest_path = nx.average_shortest_path_length(graph)
        print('average shortest path: ', average_shortest_path)
    else:
        components = nx.connected_components(graph)
        number_connected_components = nx.number_connected_components(graph)
        average_shortest_path = 0
        for component in components:
            subgraph = graph.subgraph(component)
            sub_asp = nx.average_shortest_path_length(subgraph)
            average_shortest_path += sub_asp
        print('average shortest path: ', float(average_shortest_path / number_connected_components))

################### Degree Distribution Plot ###################

def draw_degree_distribution(graph):
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

def get_assortivity(graph):
    degree_assortativity_coefficient = nx.degree_assortativity_coefficient(graph)
    print('degree assortativity coefficient: ', "%3.1f"%degree_assortativity_coefficient)

################### Centrality 1: Degree ###################

def get_degree_centrality(graph):
    degree_centrality = nx.degree_centrality(graph)
    res = sorted(degree_centrality.items(), key=lambda kv: kv[1])
    print('top 5 at degree centrality: ', res[::-1][0:5])
    length = len(res)
    max_diff = res[length-1][1] - res[0][1]
    all_diff = 0
    for dc in res:
        all_diff += res[length-1][1] - dc[1]
    print('degree centralization (based on freeman formula): ', float(all_diff/(max_diff*length)))

################### Centrality 2: Closeness ###################

def get_closeness_centrality(graph):
    closeness_centrality = nx.closeness_centrality(graph)
    res = sorted(closeness_centrality.items(), key=lambda kv: kv[1])
    print('top 5 at closeness centrality: ', res[::-1][0:5])
    length = len(res)
    max_diff = res[length-1][1] - res[0][1]
    all_diff = 0
    for dc in res:
        all_diff += res[length-1][1] - dc[1]
    print('closeness centralization (based on freeman formula): ', float(all_diff/(max_diff*length)))

################### Centrality 3: Betweenness ###################

def get_betweenness_centrality(graph):
    betweenness_centrality = nx.betweenness_centrality(graph)
    res = sorted(betweenness_centrality.items(), key=lambda kv: kv[1])
    print('top 5 at betweenness centrality: ', res[::-1][0:5])
    length = len(res)
    max_diff = res[length-1][1] - res[0][1]
    all_diff = 0
    for dc in res:
        all_diff += res[length-1][1] - dc[1]
    print('betweenness centralization (based on freeman formula): ', float(all_diff/(max_diff*length)))

################### Generate Custom Graph ###################

def create_custom_graph():
    g = nx.Graph()
    g.add_node('plant')
    g.add_node('rabbit')
    g.add_node('squirrel')
    g.add_node('mice')
    g.add_node('bird')
    g.add_node('herbivorous insect')
    g.add_node('predaceous insect')
    g.add_node('spider')
    g.add_node('toad')
    g.add_node('insectivirous bird')
    g.add_node('snake')
    g.add_node('hawk')
    g.add_node('owl')
    g.add_node('fox')
    g.add_edge('plant', 'rabbit')
    g.add_edge('plant', 'squirrel')
    g.add_edge('plant', 'mice')
    g.add_edge('plant', 'bird')
    g.add_edge('plant', 'herbivorous insect')
    g.add_edge('rabbit', 'fox')
    g.add_edge('rabbit', 'hawk')
    g.add_edge('rabbit', 'owl')
    g.add_edge('squirrel', 'fox')
    g.add_edge('squirrel', 'hawk')
    g.add_edge('squirrel', 'owl')
    g.add_edge('mice', 'fox')
    g.add_edge('mice', 'snake')
    g.add_edge('mice', 'hawk')
    g.add_edge('mice', 'owl')
    g.add_edge('bird', 'fox')
    g.add_edge('bird', 'hawk')
    g.add_edge('bird', 'owl')
    g.add_edge('bird', 'snake')
    g.add_edge('herbivorous insect', 'spider')
    g.add_edge('herbivorous insect', 'insectivirous bird')
    g.add_edge('herbivorous insect', 'predaceous insect')
    g.add_edge('herbivorous insect', 'snake')
    g.add_edge('spider', 'insectivirous bird')
    g.add_edge('spider', 'predaceous insect')
    g.add_edge('predaceous insect', 'toad')
    g.add_edge('predaceous insect', 'snake')
    g.add_edge('predaceous insect', 'insectivirous bird')
    g.add_edge('predaceous insect', 'spider')
    g.add_edge('insectivirous bird', 'snake')
    g.add_edge('insectivirous bird', 'hawk')
    g.add_edge('insectivirous bird', 'owl')
    g.add_edge('insectivirous bird', 'fox')
    g.add_edge('toad', 'snake')
    return g

################### Erdős-Rényi Graph ###################

def generate_erdos_renyi_graph(graph, filename):
    print('######################################')
    print('Generating Erdős-Rényi Graph...')
    print('######################################')
    number_of_nodes = graph.number_of_nodes()
    prob_dics = {'food_web': 0.5, 'facebook': 0.01, 'physics': 0.0011}
    random_net = nx.erdos_renyi_graph(n=number_of_nodes, p=prob_dics[filename])
    calculate_graph_metrics(random_net)

################### Watts-Strogatz Graph ###################

def generate_watts_strogatz_graph(graph, filename):
    print('######################################')
    print('Generating Watts-Strogatz Graph...')
    print('######################################')
    number_of_nodes = graph.number_of_nodes()
    prob_dics = {'food_web': 0.6, 'facebook': 0.01, 'physics': 0.0015}
    nearest_neighbors_dict = {'food_web': 5, 'facebook': 44, 'physics': 21}
    random_net = nx.watts_strogatz_graph(n=number_of_nodes, k=nearest_neighbors_dict[filename], p=prob_dics[filename])
    calculate_graph_metrics(random_net)

################### Barabasi-Albert Graph ###################

def generate_barabasi_albert_graph(graph, filename):
    print('######################################')
    print('Generating Barabasi-Albert Graph...')
    print('######################################')
    number_of_nodes = graph.number_of_nodes()
    attachment_dict = {'food_web': 3, 'facebook': 22, 'physics': 10}
    random_net = nx.barabasi_albert_graph(n=number_of_nodes, m=attachment_dict[filename])
    calculate_graph_metrics(random_net)

################### Random-Kernel Graph ###################

def integral(u, w, z):
    c = 1
    return c * (z - w)

def root(u, w, z):
    c = 1
    return r / c + w

def generate_random_kernel_graph(graph, filename):
    print('######################################')
    print('Generating Random-Kernel Graph...')
    print('######################################')
    number_of_nodes = graph.number_of_nodes()
    random_net = nx.random_kernel_graph(number_of_nodes, integral, root)
    calculate_graph_metrics(random_net)

################### Girvan-Newman Algorithm ###################

def detect_girvan_newman_communities(graph):
    print('######################################')
    print('Detecting Communities based on Girvan-Newman algorithm...')
    print('######################################')
    components = community.girvan_newman(graph)
    community_tuple = tuple(sorted(c) for c in next(components))
    print('communities are: ', community_tuple)
    print('######################################')
    print('Calculating Modularity...')
    print('######################################')
    modularity = community.modularity(graph, next(components))
    print('modularity is: ', modularity)
    print('######################################')
    print('Drawing Communities...')
    print('######################################')
    pos = nx.spring_layout(graph)
    i = 0
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))
    cs = get_colors(len(community_tuple))
    for nodes in community_tuple:
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_color=cs[i])
        i += 1
    plt.show()

################### Clauset-Newman-Moore Algorithm ###################

def detect_clauset_newman_moore_communities(graph):
    print('######################################')
    print('Detecting Communities based on Clauset-Newman-Moore algorithm...')
    print('######################################')
    components = community.greedy_modularity_communities(graph)
    community_tuple = tuple(sorted(c) for c in list(components))
    print('communities are: ', community_tuple)
    print('######################################')
    print('Calculating Modularity...')
    print('######################################')
    modularity = community.modularity(graph, components)
    print('modularity is: ', modularity)
    print('######################################')
    print('Drawing Communities...')
    print('######################################')
    pos = nx.spring_layout(graph)
    i = 0
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF),range(n)))
    cs = get_colors(len(community_tuple))
    for nodes in community_tuple:
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_color=cs[i])
        i += 1
    plt.show()

################### SIR Epidemic model on Erdős-Rényi ###################

def simulate_sir_on_erdos_renyi():
    print('######################################')
    print('Simulating SIR Model on Erdős-Rényi Graph...')
    print('######################################')
    g = nx.erdos_renyi_graph(1000, 0.15)
    model = sir.SIRModel(g)
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.01)
    cfg.add_model_parameter('gamma', 0.005)
    cfg.add_model_parameter("fraction_infected", 0.05)
    model.set_initial_status(cfg)
    iterations = model.iteration_bunch(200)
    trends = model.build_trends(iterations)
    draw_epidemic_plot(model, trends)

################### SIR Epidemic model on Barabasi-Albert  ###################

def simulate_sir_on_barabasi_albert():
    print('######################################')
    print('Simulating SIR Model on Barabasi-Albert Graph...')
    print('######################################')
    g = nx.barabasi_albert_graph(1000, 10)
    model = sir.SIRModel(g)
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.01)
    cfg.add_model_parameter('gamma', 0.005)
    cfg.add_model_parameter("fraction_infected", 0.05)
    model.set_initial_status(cfg)
    iterations = model.iteration_bunch(200)
    trends = model.build_trends(iterations)
    draw_epidemic_plot(model, trends)

################### SI Epidemic model on Erdős-Rényi ###################

def simulate_si_on_erdos_renyi():
    print('######################################')
    print('Simulating SI Model on Erdős-Rényi Graph...')
    print('######################################')
    g = nx.erdos_renyi_graph(1000, 0.15)
    model = si.SIModel(g)
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.01)
    cfg.add_model_parameter("fraction_infected", 0.05)
    model.set_initial_status(cfg)
    iterations = model.iteration_bunch(200)
    trends = model.build_trends(iterations)
    draw_epidemic_plot(model, trends)

################### SI Epidemic model on Barabasi-Albert ###################

def simulate_si_on_barabasi_albert():
    print('######################################')
    print('Simulating SI Model on Barabasi-Albert Graph...')
    print('######################################')
    g = nx.barabasi_albert_graph(1000, 10)
    model = si.SIModel(g)
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.01)
    cfg.add_model_parameter("fraction_infected", 0.05)
    model.set_initial_status(cfg)
    iterations = model.iteration_bunch(200)
    trends = model.build_trends(iterations)
    draw_epidemic_plot(model, trends)

################### Epidemic model Draw ###################

def draw_epidemic_plot(model, trends):
    viz = DiffusionTrend(model, trends)
    p = viz.plot(width=650, height=500)
    viz2 = DiffusionPrevalence(model, trends)
    p2 = viz2.plot(width=650, height=500)
    vm = MultiPlot()
    vm.add_plot(p)
    vm.add_plot(p2)
    m = vm.plot()
    show(m)

###################################### Excecution ######################################

def calculate_graph_metrics(graph):
    print('######################################')
    print('Calculating Graph Metrics...')
    print('######################################')
    get_number_of_nodes(graph)
    get_number_of_edges(graph)
    get_average_degree(graph)
    get_density(graph)
    get_first_cc(graph)
    get_second_cc(graph)
    get_diameter(graph)
    get_average_shortest_path(graph)
    get_assortivity(graph)
    get_degree_centrality(graph)
    get_closeness_centrality(graph)
    get_betweenness_centrality(graph)
    draw_degree_distribution(graph)

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('please pass a parameter')
    else:
        if sys.argv[1] == 'simulate':
            if sys.argv[2] == 'si' and sys.argv[3] == 'erdos_renyi':
                simulate_si_on_erdos_renyi()
            elif sys.argv[2] == 'sir' and sys.argv[3] == 'erdos_renyi':
                simulate_sir_on_erdos_renyi()
            elif sys.argv[2] == 'si' and sys.argv[3] == 'barabasi_albert':
                simulate_si_on_barabasi_albert()
            elif sys.argv[2] == 'sir' and sys.argv[3] == 'barabasi_albert':
                simulate_sir_on_barabasi_albert()
            else:
                print('invalid input for simulation epidemic model')
                exit(0)
        else:
            graph = None
            if sys.argv[2] == 'food_web':
                filename = 'food_web'
                graph = create_custom_graph()
            else:
                filename = DATASET_FOLDER + sys.argv[2] + '.txt'
                if os.path.exists(filename):
                    graph = nx.read_edgelist(filename, create_using=nx.Graph(), nodetype=int)
                else:
                    print('file not found. check your input parameter')
            if graph is None:
                print('can not build graph')
                exit(0)
            if sys.argv[1] == 'calculate':
                calculate_graph_metrics(graph)
            elif sys.argv[1] == 'generate':
                if len(sys.argv) <= 3:
                    print('please pass a random graph type')
                elif sys.argv[3] == 'erdos_renyi':
                    generate_erdos_renyi_graph(graph, sys.argv[2])
                elif sys.argv[3] == 'watts_strogatz':
                    generate_watts_strogatz_graph(graph, sys.argv[2])
                elif sys.argv[3] == 'barabasi_albert':
                    generate_barabasi_albert_graph(graph, sys.argv[2])
                elif sys.argv[3] == 'random_kernel':
                    generate_random_kernel_graph(graph, sys.argv[2])
                else:
                    print('invalid random graph type')
            elif sys.argv[1] == 'community_detect':
                if len(sys.argv) <= 3:
                    print('please pass a community detection algorithm')
                elif sys.argv[3] == 'girvan_newman':
                    detect_girvan_newman_communities(graph)
                elif sys.argv[3] == 'clauset_newman_moore':
                    detect_clauset_newman_moore_communities(graph)
                else:
                    print('invalid community detection algorithm')
            else:
                print('invalid command')
            
