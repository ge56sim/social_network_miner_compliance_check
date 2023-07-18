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
This file creates a json document for the graph structure implemented and
can be used for graph objects created base on a text or event log.
"""

import json


def save_graphs_to_json_text(graphs: list, file_name: str, output_path):
    data = {}

    for i, graph in enumerate(graphs, start=1):
        graph_name = f"graph_{i:02d}"
        nodes = [{"resource": node} for node in graph[0]]
        edges = [{"resource_performer": edge[0], "resource_consumer": edge[1], "activity": edge[2]} for edge in
                 graph[1]]

        graph_data = {"nodes": nodes, "edges": edges}
        data[graph_name] = graph_data

    # JSON converter:
    json_output = json.dumps(data, ensure_ascii=False, indent=4, default=str)
    # Write results in new .json file in output folder
    with open((output_path + file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

        return json_output


def save_graphs_to_json_event_log(graphs: list, file_name: str, output_path):
    data = {}

    for i, graph in enumerate(graphs, start=1):
        graph_name = f"graph_{i:02d}"
        nodes = [{"resource": node} for node in graph['graph'][0]]
        edges = [{"resource_performer": edge[0], "resource_consumer": edge[1], "activity": edge[2]} for edge in
                 graph['graph'][1]]

        graph_data = {'case_ids': graph['case_ids'], "nodes": nodes, "edges": edges}
        data[graph_name] = graph_data

    # JSON converter:
    json_output = json.dumps(data, ensure_ascii=False, indent=4, default=str)
    # Write results in new .json file in output folder
    with open((output_path + file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

        return json_output
