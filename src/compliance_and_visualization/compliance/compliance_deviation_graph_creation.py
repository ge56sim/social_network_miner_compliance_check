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
The file returns the trace graph and the compliance deviation graph
based on a comparison of the nodes and edges of the two graphs
"""


def create_compliance_deviating_graphs(trace_graph: tuple[list, list[tuple]],
                                       matched_gt_graph: tuple[list, list[tuple]]):
    trace_nodes, trace_edges = trace_graph
    matched_gt_nodes, matched_gt_edges = matched_gt_graph

    unique_edges = []

    # make all edges to lowercase and remove activity:
    trace_edges_to_compare = [(res_p.lower(), res_c.lower()) for (res_p, res_c, act) in trace_edges]
    matched_gt_edges_to_compare = [(res_p.lower(), res_c.lower()) for (res_p, res_c, act) in matched_gt_edges]

    for i, edge in enumerate(trace_edges_to_compare, start=0):
        if edge not in matched_gt_edges_to_compare:
            unique_edges.append(trace_edges[i])

    compliance_deviation_graph = (trace_nodes, unique_edges)

    return compliance_deviation_graph
