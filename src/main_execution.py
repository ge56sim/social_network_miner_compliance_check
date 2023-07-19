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
This file is responsible for execution. Run this file to execute the whole social mining process from text, event logs
and a corresponding compliance check
"""

import os

from dotenv import load_dotenv

# Imports for event log pre-processing
from social_network_generation.social_network_generation_event_log.pre_processing.pre_process_event_log_generator import \
    create_network_distinct_traces_of_event_log_pre_process_json

# Create graph data structure from pre-processed text
from social_network_generation.social_network_generation_text.graph_construction.transform_pre_process_to_graph import \
    create_graph as create_graph_from_text

# Create graph data structure from pre-processed event log
from social_network_generation.social_network_generation_event_log.graph_construction.transform_pre_process_to_graph import \
    create_graph as create_graph_from_event_log

# Create json form graph data:
from social_network_generation.create_json_from_graphs import save_graphs_to_json_text, save_graphs_to_json_event_log

# check compliance deviation
from compliance_and_visualization.compliance.compliance_deviation_graph_creation import \
    create_compliance_deviating_graphs
from compliance_and_visualization.compliance.trace_and_gt_graph_matching import match_trace_with_ground_truths

# visualize the graph structure
from compliance_and_visualization.visualization.visualizer import visualize_directed_graph, \
    visualize_cluster_of_graph, visualize_compliance_detecting_graph


def setup_environment():
    # Load environment variables from the .env file
    load_dotenv()
    return os.environ['HOME_PATH']


# Pre-Processes the Event Log data and creates a json file out of it with network information of every trace
def pre_process_event_log(log_file_path: str,
                          case_id_column_name: str,
                          activity_column_name: str,
                          timestamp_key_name: str,
                          resource_key_name: str,
                          used_separator: str,
                          home_path: str,
                          file_name: str,
                          output_path: str
                          ):
    # Create pre-processed output file for specified log: Bicycle:
    create_network_distinct_traces_of_event_log_pre_process_json(dataframe_input_path=log_file_path,
                                                                 case_id_column_name=case_id_column_name,
                                                                 activity_column_name=activity_column_name,
                                                                 timestamp_key_name=timestamp_key_name,
                                                                 resource_key_name=resource_key_name,
                                                                 used_separator=used_separator,
                                                                 file_name=file_name,
                                                                 output_path=home_path + output_path
                                                                 )

    output_path_pre_process = home_path + output_path + file_name + ".json"
    return output_path_pre_process


# Constructs the graph out of the pre-processed text file
def graph_construction_text(pre_processed_text_path: str):
    list_of_gt_graphs = create_graph_from_text(json_file_path=pre_processed_text_path)
    return list_of_gt_graphs


# Constructs the graph out of the pre-processed log
def graph_construction_event_log(pre_processed_event_log_path: str, event_log_path: str, output_path_petri_net: str):
    list_of_trace_graphs = create_graph_from_event_log(json_file_path=pre_processed_event_log_path,
                                                       event_log_file_path=event_log_path,
                                                       file_path_store_petri_net=output_path_petri_net)
    return list_of_trace_graphs


# Visualizes the graphs created. Two different visualizations exist
# 1. A standard directed graph
# 2. A directed graph surrounded by clusters indicating if a cycle between nodes exist
def visualization_graphs(graph_list: list,
                         home_path: str,
                         output_file_name: str,
                         relative_output_path_visualizations_standard: str,
                         relative_output_path_visualizations_clusters: str,
                         type_input: str):
    counter = 0

    for graph in graph_list:
        if type_input == 'text':
            node_list = graph[0]
            edge_list = graph[1]
        elif type_input == 'event_log':
            node_list = graph['graph'][0]
            edge_list = graph['graph'][1]
        else:
            raise ValueError('Wrong type is given!')

        visualize_directed_graph(vertices=node_list,
                                 edges=edge_list,
                                 output_path=home_path + relative_output_path_visualizations_standard,
                                 output_file_name=output_file_name + "_trace_" + str(counter)
                                 )

        visualize_cluster_of_graph(vertices=node_list,
                                   edges=edge_list,
                                   output_path=home_path + relative_output_path_visualizations_clusters,
                                   output_file_name=output_file_name + "_trace_" + str(counter)
                                   )
        counter = counter + 1


# Visualizes the compliance deviation
def visualization_compliance_deviation(graph_trace: tuple[list, list[tuple]],
                                       graph_deviations: tuple[list, list[tuple]],
                                       home_path: str,
                                       file_name: str,
                                       relative_output_path_compliance_deviations: str):
    visualize_compliance_detecting_graph(vertices_log=graph_trace[0],
                                         edges_log=graph_trace[1],
                                         compliance_deviating_vertices=graph_deviations[0],
                                         compliance_deviating_edges=graph_deviations[1],
                                         output_path=home_path + relative_output_path_compliance_deviations,
                                         output_file_name=file_name
                                         )


# This main method executes the whole process in one run
def execute_social_network_mining_compliance_deviation_process():
    # General Home, Absolute Path
    home_path = setup_environment()

    # TODO: Event Log File Paths:
    # Input Synthetic Event Logs:
    # BM
    path_log_bm = "/data/input/log/selected/BM_event_log.csv"
    log_file_path_bm = home_path + path_log_bm
    # SM:
    # path_log_sm = "/data/input/log/selected/SM_event_log.csv"
    # log_file_path_sm = home_path + path_log_sm
    # RE:
    # path_log_re = "/data/input/log/selected/RE_event_log.csv"
    # log_file_path_re = home_path + path_log_re
    # BPIC:
    # path_log_bpic = "/data/input/log/selected/BPIC_event_log.csv"
    # log_file_path_bpic = home_path + path_log_bpic

    # 1. Pre-Process Text
    # This is already done with an LLM, the pre-processed file is already stored in the data output folder
    # TODO: Pre-Processed Text files:
    # BM
    path_pre_processed_text_bm = home_path + '/data/output/01_pre_processing_text/BM_pre_processed.json'
    # SM
    # path_pre_processed_text_sm = home_path + '/data/output/01_pre_processing_text/SM_pre_processed.json'
    # RE
    # path_pre_processed_text_re = home_path + '/data/output/01_pre_processing_text/RE_pre_processed.json'
    # BPIC
    # path_pre_processed_text_bpic2020 = home_path + '/data/output/01_pre_processing_text/BPIC_pre_processed.json'

    # 2. Pre-Process Event Log

    # Required data:
    # TODO: Change the log file path to the appropriate, currently ..._bm
    log_file_path = log_file_path_bm
    case_id_column_name = 'concept:instance'
    activity_column_name = 'concept:name'
    timestamp_key_name = 'time:timestamp'

    # Check the resource key name, sometimes it can be the case that role is used sometimes it can be the case that unit is used
    resource_key_name = 'Organizational_Unit'
    used_separator = ','

    # TODO: Output File Name Pre-Processed Event Log:
    # BM
    file_name_bm_pre_process_event_log = 'BM_pre_processed'
    # SM
    # file_name_sm_pre_process_event_log = 'SM_pre_processed'
    # RE
    # file_name_re_pre_process_event_log = 'RE_pre_processed'
    # BPIC
    # file_name_bpic_pre_process_event_log = 'bpic_pre_processed'

    output_path_pre_process = '/data/output/02_pre_processing_event_log/'

    # TODO: change the file_name
    path_pre_processed_event_log = pre_process_event_log(log_file_path=log_file_path,
                                                         case_id_column_name=case_id_column_name,
                                                         activity_column_name=activity_column_name,
                                                         timestamp_key_name=timestamp_key_name,
                                                         resource_key_name=resource_key_name,
                                                         used_separator=used_separator,
                                                         home_path=home_path,
                                                         file_name=file_name_bm_pre_process_event_log,
                                                         output_path=output_path_pre_process
                                                         )

    # 3. Graphs constructed from the text

    # TODO: Graph data of Text:
    # BM
    graphs_text_bm = graph_construction_text(pre_processed_text_path=path_pre_processed_text_bm)
    # SM
    # graphs_text_sm = graph_construction_text(pre_processed_text_path=path_pre_processed_text_sm)
    # RE
    # graphs_text_re = graph_construction_text(pre_processed_text_path=path_pre_processed_text_bm)
    # BPIC
    # graphs_text_bpic2020 = graph_construction_text(pre_processed_text_path=path_pre_processed_text_bpic2020)

    # Store the graphs persistently
    # TODO: Output File Names for Text Graph:
    # BM
    graph_text_file_name_bm = "BM_graphs"
    # SM
    # graph_text_file_name_sm = "SM_graphs"
    # RE
    # graph_text_file_name_re = "RE_graphs"
    # BPIC
    # graph_text_file_name_bpic2020 = "BPIC2020_graphs"

    output_path_graphs_text = home_path + "/data/output/03_snm_t/"

    # Change Parameters to create the graphs for each description
    save_graphs_to_json_text(graphs=graphs_text_bpic2020,
                             file_name=graph_text_file_name_bm,
                             output_path=output_path_graphs_text)

    # 4. Graphs constructed from the event log

    # TODO: Output File Names for Event Log Graph:
    # BM
    graphs_event_log_file_name_bm = "BM_graphs"
    # SM
    # graphs_event_log_file_name_sm = "SM_graphs"
    # RE
    # graphs_event_log_file_name_re = "RE_graphs"
    # BPIC
    # graphs_event_log_file_name_bpic = "BPIC_graphs"

    # TODO: Output File Names for Petri Net:
    # BM
    output_path_petri_net_bm = home_path + '/data/output/04_snm_el/petri_net_of_event_log/' + 'BM_petri_net.svg'
    # SM
    # output_path_petri_net_sm = home_path + '/data/output/04_snm_el/petri_net_of_event_log/' + 'SM_petri_net.svg'
    # RE
    # output_path_petri_net_re = home_path + '/data/output/04_snm_el/petri_net_of_event_log/' + 'RE_petri_net.svg'
    # BPIC
    # output_path_petri_net_bpic = home_path + '/data/output/04_snm_el/petri_net_of_event_log/' + 'BPIC_petri_net.svg'

    # General output path of graphs from event log
    output_path_petri_graphs_event_log = home_path + "/data/output/04_snm_el/graphs/"

    graphs_event_log = graph_construction_event_log(pre_processed_event_log_path=path_pre_processed_event_log,
                                                    event_log_path=log_file_path_re,
                                                    output_path_petri_net=output_path_petri_net_bm
                                                    )

    # Change Parameters to create the graphs for each trace in log
    save_graphs_to_json_event_log(graphs=graphs_event_log,
                                  file_name=graphs_event_log_file_name_bm,
                                  output_path=output_path_petri_graphs_event_log)

    #
    # 5. Visualizations Graphs Text

    # TODO: Output File Names for standard and cluster visualization:
    # BM
    visualization_file_name_text_bm = "BM_text"
    visualization_file_name_event_log_bm = "BM_event_log"
    # SM
    # visualization_file_name_text_sm = "SM_text"
    # visualization_file_name_event_log_sm = "SM_event_log"
    # RE
    # visualization_file_name_text_re = "RE_text"
    # visualization_file_name_event_log_re = "RE_event_log"
    # BPIC
    # visualization_file_name_text_bpic = "BPIC_text"
    # visualization_file_name_event_log_bpic = "BPIC_event_log"

    # Output paths
    # Text
    relative_output_path_visualizations_standard_text = "/data/output/05_visualization/standard/text/"
    relative_output_path_visualizations_clusters_text = "/data/output/05_visualization/clusters_included/text/"
    # Event Log
    relative_output_path_visualizations_standard_event_log = "/data/output/05_visualization/standard/event_log/"
    relative_output_path_visualizations_clusters_event_log = "/data/output/05_visualization/clusters_included/event_log/"

    # Graph 05_visualization Text
    visualization_graphs(graph_list=graphs_text_bm,
                         home_path=home_path,
                         output_file_name=visualization_file_name_text_bm,
                         relative_output_path_visualizations_standard=relative_output_path_visualizations_standard_text,
                         relative_output_path_visualizations_clusters=relative_output_path_visualizations_clusters_text,
                         type_input='text')

    # Graph 05_visualization event log
    visualization_graphs(graph_list=graphs_event_log,
                         home_path=home_path,
                         output_file_name=visualization_file_name_event_log_bm,
                         relative_output_path_visualizations_standard=relative_output_path_visualizations_standard_event_log,
                         relative_output_path_visualizations_clusters=relative_output_path_visualizations_clusters_event_log,
                         type_input='event_log')

    # 6 & 7. Compliance Deviation Creation & Visualization Compliance deviation Graphs

    # TODO: Output File Names for compliance deviation visualization:
    # BM
    output_file_name_comp_dev_bm = "BM_compliance_deviation_graph_trace"
    # SM
    # output_file_name_comp_dev_sm = "SM_compliance_deviation_graph_trace"
    # RE
    # output_file_name_comp_dev_re = "RE_compliance_deviation_graph_trace"
    # BPIC
    # output_file_name_comp_dev_bpic = "BPIC_compliance_deviation_graph_trace"

    relative_output_path_visualizations_cd = "/data/output/05_visualization/compliance_deviations/"

    # Iterate through all trace graphs:
    # Bicycle:
    for i, data in enumerate(graphs_event_log, start=1):
        trace_graph = data['graph']

        trace_graph, matched_gt_graph = match_trace_with_ground_truths(trace_graph=trace_graph,
                                                                       list_of_ground_truths=graphs_text_bm)

        deviating_graph_bm = create_compliance_deviating_graphs(trace_graph=trace_graph,
                                                                matched_gt_graph=matched_gt_graph)

        visualization_compliance_deviation(graph_trace=trace_graph,
                                           graph_deviations=deviating_graph_bm,
                                           home_path=home_path,
                                           file_name=output_file_name_comp_dev_bm + str(i),
                                           relative_output_path_compliance_deviations=relative_output_path_visualizations_cd
                                           )


if __name__ == "__main__":
    execute_social_network_mining_compliance_deviation_process()
