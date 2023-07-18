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
This file returns for each trace the corresponding ground truth (gt) graph
"""


def match_trace_with_ground_truths(trace_graph: tuple[list, list[tuple]],
                                   list_of_ground_truths: list[tuple[list, list[tuple]]]):
    trace_nodes, trace_edges = trace_graph

    best_match = None
    best_similarity = 0

    # make all edges to lowercase and remove activity:
    trace_edges = [(res_p.lower(), res_c.lower()) for (res_p, res_c, act) in trace_edges]

    count = 1
    for gt_graph in list_of_ground_truths:
        gt_nodes, gt_edges = gt_graph

        gt_edges_to_compare = [(res_p.lower(), res_c.lower()) for (res_p, res_c, act) in gt_edges]

        for edge in trace_edges:
            if edge in gt_edges_to_compare:
                count = count + 1

        total_similarity = 0
        # Calculate total similarity
        if len(set(gt_nodes)) > 0:
            total_similarity = count / len(set(trace_edges))

        # Update best match if the current graph has higher similarity
        if total_similarity > best_similarity:
            best_match = gt_graph
            best_similarity = total_similarity

    return trace_graph, best_match
