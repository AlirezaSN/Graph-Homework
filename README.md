# Dynamic Complex Network Assignment #5

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

In order to generate random graphs like `Erdős-Rényi`, `Watts-Strogatz`, `Barabasi-Albert` and `Random-Kernel` run this:

```
$ python3 main.py generate <DATASET_FILE> <RANDOM_GRAPH_TYPE>
```

**DATASET_FILE** can be `facebook`, `physics` and `food_web`.

**RANDOM_GRAPH_TYPE** can be `erdos_renyi`, `watts_strogatz`, `barabasi_albert` and `random_kernel`.

## Detect Communities

In order to detect and plot communities and calculate modularity run this:

```
$ python3 main.py community_detect <DATASET_FILE> <COMMUNITY_DETECTION_ALGORITHM>
```

**DATASET_FILE** can be `facebook`, `physics` and `food_web`.

**COMMUNITY_DETECTION_ALGORITHM** can be `girvan_newman` and `clauset_newman_moore`.

## Simulate Epidemic Models

In order to simulate epidemic models, run this:

```
$ python3 main.py simulate <EPIDEMIC_MODEL> <RANDOM_GRAPH_MODEL>
```

**EPIDEMIC_MODEL** can be `si` and `sir`

**RANDOM_GRAPH_MODEL** can be `erdos_renyi` and `barabasi_albert`