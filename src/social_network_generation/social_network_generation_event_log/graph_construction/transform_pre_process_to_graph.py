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
This file provides methods that transforms the json document to a graph data structure.
"""

import json
import pm4py
import pandas as pd


def create_graph(json_file_path: str, event_log_file_path: str, file_path_store_petri_net: str):
    # Output List:
    trace_network_results = []

    # list of network structure for each trace:
    structure_list = __get_list_from_json(json_file_path=json_file_path)

    # List that stores all and nodes of process
    list_of_and_branches = __get_parallel_activities_from_petri_net(event_log_file_path=event_log_file_path,
                                                                    file_path_store_petri_net=file_path_store_petri_net
                                                                    )
    print(list_of_and_branches)

    # Go through every trace and create a network for every trace:
    for structure in structure_list:
        structure_network = structure['network_trace']

        node_list = __create_nodes(structure_network=structure_network)
        edge_list = __create_edges(structure_network=structure_network, list_of_and_cases=list_of_and_branches)

        # List of graphs for each trace as tuple:
        # Additionally return id and corresponding case ids for each trace
        trace_network_results.append(
            {'id': structure['id'], 'case_ids': structure['case_ids'], 'graph': (node_list, edge_list)})

    return trace_network_results


# Creates nodes from the json pre-process document
# @private
def __create_nodes(structure_network: list[dict]):
    # Output List:
    node_list = []
    for network_value in structure_network:
        # Check if resource == consumer:
        if network_value["Resource Performer"] == network_value["Resource Consumer"] and \
                network_value["Resource Consumer"] != "":
            # Add node only to network if it is not already in list:
            if network_value["Resource Consumer"] not in node_list:
                node_list.append(network_value["Resource Consumer"])
        else:
            if network_value["Resource Performer"] not in node_list and network_value["Resource Performer"] != "":
                node_list.append(network_value["Resource Performer"])

            if network_value["Resource Consumer"] not in node_list and network_value["Resource Consumer"] != "":
                node_list.append(network_value["Resource Consumer"])
    return node_list


def __create_edges(structure_network: list[dict], list_of_and_cases: list):
    # Output List
    edge_list = []
    # Check list:
    activities_checked = []
    # Go through values in the network
    for network_value in structure_network:
        # Activity will not check in and loop
        activity_in_and_checked = False
        # Check if Activity was already checked
        if network_value in activities_checked:
            continue
        else:
            # Current Activity
            activity = network_value["Activity"]

            # Go through and activity case and check if it is inside:
            for and_case in list_of_and_cases:
                start_activity = and_case["start_activity"]
                if activity == start_activity:

                    # Process that adds several interactions for n consumers based on "and" start activity
                    # Check if resource == "" (performer):
                    if network_value["Resource Performer"] != "":
                        performer = network_value["Resource Performer"]
                        consumers = []

                        # Go through the list of begin events:
                        for begin_of_path_activity in and_case['list_of_begin_and_branch_activities']:
                            for value_helper in structure_network:
                                if value_helper['Activity'] == begin_of_path_activity:
                                    consumers.append(value_helper['Resource Performer'])

                        # Add to edges start of and activity n times, depending on how many and branches, paths
                        for consumer in consumers:
                            if consumer != "":
                                edge_list.append((performer, consumer, activity))

                        # Add activity to checked activity:
                        activities_checked.append(activity)

                    # TODO
                    # Follow-up list of activities:
                    # Only relevant if the lists store more than one element, otherwise process stops here
                    for follow_up_paths in and_case['list_of_and_path']:
                        if len(follow_up_paths) > 1:
                            # Go through the activities
                            for activity_follow_up in follow_up_paths:
                                None
                                # finished here do nothing more

                    # Remove case of list of and cases
                    # list_of_and_cases.remove(and_case)

                    # Indicator that activity was already checked in loop:
                    activity_in_and_checked = True

            if not activity_in_and_checked:
                if network_value["Resource Performer"] != "" and network_value["Resource Consumer"] != "":
                    edge_list.append((network_value["Resource Performer"], network_value["Resource Consumer"],
                                      network_value["Activity"]))

                # Nothing more to implement?
                # Only in the logic the consumer of the start event changes in the "and"-case when iterating through the log.
                # Does also something change in the follow-up part and at the end activity?
                # -> Follow up the activity has a predefined performer and consumer -> which can in n scenarios differ

    return edge_list


# Check from the petri net the activities that are executed in parallel:
def __get_parallel_activities_from_petri_net(event_log_file_path: str, file_path_store_petri_net: str):
    # Get alpha miner petri net and bpmn:
    net, initial_marking, final_marking = alpha_miner(event_log_file_path=event_log_file_path,
                                                      file_path_store_petri_net=file_path_store_petri_net)

    # Fill information about and branches in log
    list_and_in_branch = []
    # Values stored in dict for each branch path
    start_activity = ""
    list_of_in_and_branch_start_activity = []
    list_of_and_branches = []
    end_event_arcs = ""

    transitions = net.transitions
    # Iterate through the list of transitions
    for transition in transitions:

        # And branch found
        if len(transition.out_arcs) > 1:
            start_event_and = transition.name
            # Store first in and branch event
            list_of_in_and_branch_start_activities = []
            for in_and_activity in transition.out_arcs:

                # only if the activity is given:
                if len(list(in_and_activity.target.out_arcs)) > 0:
                    # Name of activity (transition) that is the first of the n in and branches
                    in_and_branch = list(in_and_activity.target.out_arcs)[0].target.name
                    # Add the first nodes in and branch to the list
                    list_of_in_and_branch_start_activities.append(in_and_branch)

            if len(list_of_in_and_branch_start_activities) > 0:

                # After the list of in branches is filled, fill list of next activities within a branch
                # List of lists, either this list is empty, or for every and branch a list consist that stores the activities in that branch
                list_of_and_branches = []
                # Iterate through the list of first activities in respective branch:
                for list_of_in_and_branch_start_activity in list_of_in_and_branch_start_activities:

                    # List is filled with activities of the branches activity
                    intermediate_list_of_branch = [list_of_in_and_branch_start_activity]
                    # go through the whole path of the end element till end element is found:
                    end_path_found = False
                    while not end_path_found:
                        for inter in intermediate_list_of_branch:
                            # Iterate through transitions and check follow-up transition and add to list, if transition has only one incoming
                            for transition_help in transitions:
                                # Search the first follow-up activity (2nd) of the value in the list_start_activities
                                if (transition_help.name == inter and
                                        len(list(transition_help.out_arcs)) > 0
                                        and len(list(list(transition_help.out_arcs)[0].target.out_arcs)) > 0):

                                    # Name of follow-up activity
                                    # Problem this would have two n > 1 out_arcs
                                    follow_up_transition = list(list(transition_help.out_arcs)[0].target.out_arcs)[
                                        0].target.name

                                    # Check if this event has two incoming arcs
                                    for transition_help2 in transitions:
                                        if transition_help2.name == follow_up_transition:
                                            # End of and branch found
                                            if len(transition_help2.in_arcs) > 1:
                                                end_path_found = True
                                                end_event_arcs = follow_up_transition
                                                break
                                            else:
                                                # Add element to intermediate list
                                                intermediate_list_of_branch.append(follow_up_transition)
                                                break
                    # Add list of path
                    list_of_and_branches.append(intermediate_list_of_branch)

            # Fill dict with required information of one path/ branch in "and" gateway
            and_branch_dict = {'start_activity': start_event_and,
                               'list_of_begin_and_branch_activities': list_of_in_and_branch_start_activities,
                               'list_of_and_path': list_of_and_branches,
                               'end_activity': end_event_arcs}
            # Add "and" path to list
            list_and_in_branch.append(and_branch_dict)

    return list_and_in_branch


# Alpha Miner (implementation of Pm4Py)
def alpha_miner(event_log_file_path: str, file_path_store_petri_net: str):
    dataframe = pd.read_csv(event_log_file_path, sep=',')
    dataframe = pm4py.format_dataframe(dataframe,
                                       case_id='concept:instance',
                                       activity_key='concept:name',
                                       timestamp_key='time:timestamp')
    event_log = pm4py.convert_to_event_log(dataframe)
    net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)
    # pm4py.view_petri_net(net, initial_marking, final_marking)
    # save pm4py file:
    pm4py.save_vis_petri_net(petri_net=net,
                             initial_marking=initial_marking,
                             final_marking=final_marking,
                             file_path=file_path_store_petri_net)

    return net, initial_marking, final_marking


def __get_list_from_json(json_file_path: str):
    # Get Json
    with open(json_file_path) as json_file:
        pre_processed_event_log = json.load(json_file)
    # Get pre-processed textual_description data
    structure_list = pre_processed_event_log["pairs"]
    return structure_list
