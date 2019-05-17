# Dynamic Complex Network Assignment #3

## Installation
```
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```

## Calculate Graph Metrics

In order to calculate graph metrics such as #nodes, #edges, average degree, density, centralities, degree distribution plot, first and second clustering coefficient, etc, run this:

```
$ python3 main.py calculate <DATASET_FILE>
```

**DATASET_FILE** can be `facebook`, `physics` and `food_web`.

## Generate Famous Random Graphs

In order to generate random graphs like `Erdős-Rényi`, `Watts-Strogatz`, `Barabasi-Albert`, run this:

```
$ python3 main.py generate <DATASET_FILE> <RANDOM_GRAPH_TYPE>
```

**RANDOM_GRAPH_TYPE** can be `erdos_renyi`, `watts_strogatz` and `barabasi_albert`