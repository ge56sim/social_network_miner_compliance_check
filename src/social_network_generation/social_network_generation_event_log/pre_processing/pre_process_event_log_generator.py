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
This file and the corresponding methods are responsible tp create the pre-processed event log which can be used for
resource-activity compliance verification.
"""
from pandas import DataFrame
import json

from social_network_generation.social_network_generation_event_log.pre_processing.extractors_pre_processing_event_log.extraction_to_data_frame import \
    get_data_frame
from social_network_generation.social_network_generation_event_log.pre_processing.extractors_pre_processing_event_log.extraction_to_event_log import \
    convert_df_to_event_log

"""
from social_network_generation_event_log.pre_processing.sna_statistics.sna_resource_analysis import handover_of_work, \
    subcontracting, working_together, \
    similar_activities
"""


def create_network_distinct_traces_of_event_log_pre_process_json(dataframe_input_path: str,
                                                                 case_id_column_name: str,
                                                                 activity_column_name: str,
                                                                 timestamp_key_name: str,
                                                                 resource_key_name: str,
                                                                 used_separator: str,
                                                                 file_name: str,
                                                                 output_path: str):
    # csv dataframe
    dataframe = __load_data_frame(dataframe_input_path,
                                  case_id_column_name,
                                  activity_column_name,
                                  timestamp_key_name,
                                  used_separator)
    # Event Log based on dataframe, according to XES Meta model
    event_log = convert_df_to_event_log(df=dataframe)

    # List of: Network of Resource Performer, Resource Consumer, and Activity:
    resulting_networks_of_distinct_traces = event_log.get_network_output_of_distinct_traces_in_event_log(resource_structure_type=resource_key_name)

    """
    # SNA Statistics:
    hw_data, hw_directions, \
        subc_data, subc_directions, \
        work_tog_data, work_tog_directions, \
        sim_act_data, subc_directions = __get_sna_statistics(dataframe_input_path=dataframe_input_path,
                                                             case_id_column_name=case_id_column_name,
                                                             activity_column_name=activity_column_name,
                                                             resource_key_name=resource_key_name)
    """

    # Output data
    data = {"pairs": resulting_networks_of_distinct_traces}

    # JSON converter:
    json_output = json.dumps(data, ensure_ascii=False, indent=4, default=str)
    # Write results in new .json file in output folder
    with open((output_path + file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    return json_output


"""
# Return all statistics from Pm4Py in the area of social network analysis
# @private
def __get_sna_statistics(dataframe_input_path: str,
                         case_id_column_name: str,
                         activity_column_name: str,
                         resource_key_name: str):
    # Handover of work
    hw_values = handover_of_work(path_log=dataframe_input_path,
                                 case_id_name_in_log=case_id_column_name,
                                 activity_name_in_log=activity_column_name,
                                 resource_key=resource_key_name)
    hw_data = hw_values.connections
    hw_directions = hw_values.is_directed

    subc_values = subcontracting(path_log=dataframe_input_path,
                                 case_id_name_in_log=case_id_column_name,
                                 activity_name_in_log=activity_column_name,
                                 resource_key=resource_key_name)
    subc_data = subc_values.connections
    subc_directions = subc_values.is_directed

    work_tog_values = working_together(path_log=dataframe_input_path,
                                       case_id_name_in_log=case_id_column_name,
                                       activity_name_in_log=activity_column_name,
                                       resource_key=resource_key_name)
    work_tog_data = work_tog_values.connections
    work_tog_directions = work_tog_values.is_directed

    sim_act_values = similar_activities(path_log=dataframe_input_path,
                                        case_id_name_in_log=case_id_column_name,
                                        activity_name_in_log=activity_column_name,
                                        resource_key=resource_key_name)
    sim_act_data = sim_act_values.connections
    sim_act_connections = sim_act_values.is_directed

    return hw_data, hw_directions, subc_data, subc_directions, work_tog_data, work_tog_directions, sim_act_data, subc_directions
"""

"""
# Try to merge the network structure with the social network result
# @private
def __merge_network_and_statistics():
    return None
"""


# Helper method to load the data frame which is based on the XES event log
# @private
def __load_data_frame(path: str, case_id_column_name: str, activity_column_name: str,
                      timestamp_key_name: str, used_separator: str) -> DataFrame:
    # Error checking
    possible_activity_id_column_names = ["", " "]
    if case_id_column_name in possible_activity_id_column_names and not activity_column_name == type(str):
        raise ValueError("Invalid activity_check_one name.")

    possible_case_id_column_names = ["", " "]
    if case_id_column_name in possible_case_id_column_names and not case_id_column_name == type(str):
        raise ValueError("Invalid case id/ trace id name.")

    possible_separators = [";", ",", ":", "-"]
    if used_separator not in possible_separators:
        raise ValueError("Invalid separator between column values. Expected one of: %s" % possible_separators)

    print("Data Frame loaded!")
    return get_data_frame(path, case_id_column_name, activity_column_name, timestamp_key_name, used_separator)
