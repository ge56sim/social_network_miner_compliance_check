#
# This file is part of social_network_miner_compliance_check.
#
# social_network_miner_compliance_check is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# social_network_miner_compliance_check is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with social_network_miner_compliance_check (file COPYING in the main directory). If not, see
# http://www.gnu.org/licenses/.

"""
This file provides three methods that create the visualizations of the social networks.
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.table import Table


# Visualizes the flow of activities through resources
# The nodes are weighted according to the page rank algorithm
def visualize_directed_graph(vertices: list, edges: list[tuple], output_path: str, output_file_name: str):
    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from([(u, v) for u, v, _ in edges])

    #
    fixed_positions = nx.spring_layout(G, seed=3000)
    pos = nx.spring_layout(G, pos=fixed_positions, k=4, seed=3000)

    plt.figure(figsize=(16, 9))

    # Get adjusted page rank nodes
    page_rank_nodes = __get_pagerank(nodes=vertices, edges=edges)

    colormap = plt.cm.get_cmap('tab20', len(vertices))

    node_colors = [colormap(i) for i in range(len(vertices))]
    # Adjust node sizes
    node_sizes = [3000 * node[1] for node in page_rank_nodes]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, _ in edges], width=0.8, arrows=True, edge_color='black',
                           alpha=0.5, connectionstyle='arc3, rad = 0.1')

    # edge_labels = {edge[:2]: edge[2] for edge in edges}
    # Replace edge name with natural numbers
    edge_labels = {edge[:2]: i + 1 for i, edge in enumerate(edges)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in vertices}, font_color='black', font_size=10)

    plt.axis('off')

    # Create the legend table
    legend_data = [['Edge Number', 'Edge Activity']]
    for i, (_, _, activity) in enumerate(edges, start=1):
        legend_data.append([i, activity])

    ax = plt.gca()

    # Adjust the bbox to make the table narrower
    legend_table = Table(ax, bbox=[1.05, 0, 0.2, 1])
    # Adjust the scaling factor to make the table smaller
    legend_table.scale(0.7, 0.7)  # Adjust the scaling factor
    legend_table.auto_set_column_width([0, 1])

    for i, row in enumerate(legend_data):
        for j, cell in enumerate(row):
            cell_text = str(cell)
            table_cell = legend_table.add_cell(i, j, width=1, height=1, text=cell_text, loc='center', edgecolor='black')
            table_cell.set_fontsize(5)  # Adjust the font size of each cell

    ax.add_table(legend_table)

    # Adjust the compliance_and_visualization that graph and table are not intersecting
    plt.tight_layout(rect=[0, 0, 0.9, 1])

    # Store the graph
    output_file_path = output_path
    output_file_name = output_file_name + ".png"
    plt.savefig(output_file_path + output_file_name, dpi=300)

    # Show the compliance_and_visualization
    plt.show()


def visualize_cluster_of_graph(vertices: list, edges: list[tuple], output_path: str, output_file_name: str):
    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from([(u, v) for u, v, _ in edges])

    # Calculate strongly connected components
    sccs = nx.strongly_connected_components(G)
    clusters = [list(scc) for scc in sccs if len(scc) > 1]

    # Create a dictionary to map nodes to their cluster index
    cluster_mapping = {}
    for i, cluster in enumerate(clusters):
        for node in cluster:
            cluster_mapping[node] = i

    # Calculate the layout of the graph
    fixed_positions = nx.spring_layout(G, seed=3000)
    pos = nx.spring_layout(G, pos=fixed_positions, k=4, seed=3000)

    plt.figure(figsize=(12, 8))

    # Get adjusted page rank nodes
    page_rank_nodes = __get_pagerank(nodes=vertices, edges=edges)

    # Use colormap based on amount of clusters
    colormap = plt.cm.get_cmap('tab20', len(G.nodes()))

    # Node color cases
    node_colors = [colormap(i) for i in range(len(vertices))]

    # Adjust node sizes
    node_sizes = [3000 * node[1] for node in page_rank_nodes]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, _ in edges], width=0.8, arrows=True, edge_color='black',
                           alpha=0.5, connectionstyle='arc3, rad = 0.1')

    # edge_labels = {edge[:2]: edge[2] for edge in edges}
    # Replace edge name with natural numbers
    edge_labels = {edge[:2]: i + 1 for i, edge in enumerate(edges)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='grey', font_size=8)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in vertices}, font_color='black', font_size=10)

    plt.axis('off')

    # Draw clusters as circles
    for cluster in clusters:
        node_list = [node for node in cluster if node in pos]
        if len(node_list) > 1:
            node_positions = [pos[node] for node in node_list]
            center_x = sum(x for x, _ in node_positions) / len(node_positions)
            center_y = sum(y for _, y in node_positions) / len(node_positions)
            radius = max(max(abs(x - center_x), abs(y - center_y)) for x, y in node_positions)
            circle = plt.Circle((center_x, center_y), radius, facecolor='none', edgecolor='blue', linestyle='dashed')
            plt.gca().add_patch(circle)

    # Create the legend table
    legend_data = [['Edge Number', 'Edge Activity']]
    for i, (_, _, activity) in enumerate(edges, start=1):
        legend_data.append([i, activity])

    ax = plt.gca()

    # Adjust the bbox to make the table narrower
    legend_table = Table(ax, bbox=[1.05, 0, 0.2, 1])
    # Adjust the scaling factor to make the table smaller
    legend_table.scale(0.7, 0.7)  # Adjust the scaling factor
    legend_table.auto_set_column_width([0, 1])

    for i, row in enumerate(legend_data):
        for j, cell in enumerate(row):
            cell_text = str(cell)
            table_cell = legend_table.add_cell(i, j, width=1, height=1, text=cell_text, loc='center', edgecolor='black')
            table_cell.set_fontsize(5)  # Adjust the font size of each cell

    ax.add_table(legend_table)

    # Adjust the compliance_and_visualization that graph and table are not intersecting
    plt.tight_layout(rect=[0, 0, 0.9, 1])

    # Store the graph
    output_file_path = output_path
    output_file_name = output_file_name + ".svg"
    plt.savefig(output_file_path + output_file_name, dpi=300)

    # Show the compliance_and_visualization
    plt.show()


def visualize_compliance_detecting_graph(vertices_log: list, edges_log: list[tuple], compliance_deviating_vertices: list, compliance_deviating_edges: list[tuple],
                                         output_path: str, output_file_name: str):
    G = nx.DiGraph()
    G.add_nodes_from(vertices_log)
    G.add_edges_from([(u, v) for u, v, _ in edges_log])

    #
    fixed_positions = nx.spring_layout(G, seed=3000)
    pos = nx.spring_layout(G, pos=fixed_positions, k=4, seed=3000)

    plt.figure(figsize=(16, 9))

    # Get adjusted page rank nodes
    page_rank_nodes = __get_pagerank(nodes=vertices_log, edges=edges_log)

    colormap = plt.cm.get_cmap('tab20', len(vertices_log))

    node_colors = [colormap(i) for i in range(len(vertices_log))]

    # Adjust node sizes
    node_sizes = [3000 * node[1] for node in page_rank_nodes]

    # Mark the edges that are in the compliance deviating list in red, else just use black edges.
    edge_colors = ['red' if edge in compliance_deviating_edges else 'black' for edge in
                   edges_log]

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, pos, edgelist=edges_log, width=0.8, arrows=True, edge_color=edge_colors,
                           alpha=0.5, connectionstyle='arc3, rad = 0.1')

    edge_labels = {edge[:2]: i + 1 for i, edge in enumerate(edges_log)}

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=8)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in vertices_log}, font_color='black', font_size=10)

    plt.axis('off')

    # Create the legend table
    legend_data = [['Edge Number', 'Edge Activity']]
    for i, (_, _, activity) in enumerate(edges_log, start=1):
        legend_data.append([i, activity])

    ax = plt.gca()

    # Adjust the bbox to make the table narrower
    legend_table = Table(ax, bbox=[1.05, 0, 0.2, 1])
    # Adjust the scaling factor to make the table smaller
    legend_table.scale(0.7, 0.7)  # Adjust the scaling factor
    legend_table.auto_set_column_width([0, 1])

    for i, row in enumerate(legend_data):
        for j, cell in enumerate(row):
            cell_text = str(cell)
            table_cell = legend_table.add_cell(i, j, width=1, height=1, text=cell_text, loc='center', edgecolor='black')
            table_cell.set_fontsize(5)  # Adjust the font size of each cell

    ax.add_table(legend_table)

    # Adjust the compliance_and_visualization that graph and table are not intersecting
    plt.tight_layout(rect=[0, 0, 0.9, 1])

    # Store the graph
    output_file_path = output_path
    output_file_name = output_file_name + ".png"
    plt.savefig(output_file_path + output_file_name, dpi=300)

    # Show the compliance_and_visualization
    plt.show()


def __calculate_clusters(nodes, edges):
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(nodes)

    # Add edges
    G.add_edges_from(edges)

    # Calculate clusters using connected components
    clusters = list(nx.strongly_connected_components(G))

    return clusters


def __get_pagerank(nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from([(u, v) for u, v, _ in edges])

    pr = nx.pagerank(G)

    # Update nodes list with PageRank scores
    nodes = [(node, pr[node]) for node in nodes]

    # Sort nodes by PageRank score in descending order
    page_ranked_nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    return page_ranked_nodes
