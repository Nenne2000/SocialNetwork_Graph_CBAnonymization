# Project Name

## Project Description

This project involves the creation, analysis, and anonymization of bipartite graphs using Python, with a focus on social network structures. The code includes functionalities for generating synthetic data, creating bipartite graphs, and implementing class-based anonymization approaches.

## Dependencies

Make sure you have the following dependencies installed:

- pandas
- networkx
- numpy
- faker
- matplotlib

Install the dependencies using the following command:

```bash
pip install pandas networkx numpy faker matplotlib
```

## Part 1: Graph Creation and Visualization

### Running the Graph Creation Script

1. Run the graph creation script:

```bash
python create_graph.py
```

2. Follow the prompts to input the number of nodes, edges, and other parameters.

3. The script will generate synthetic data, create a bipartite graph, and save node and edge information to CSV files.

## Part 2: Class-Based Anonymization

### Running the Anonymization Script

1. Run the anonymization script:

```bash
python anonymize_graph.py --type [uniform-lists / partitioning / arbitrary-lists]
```

2. Follow the prompts to provide additional input required.

## Additional Notes

- The `VisualizeGraph.py` module is assumed to contain a function named `Visualize` for graph visualization.
