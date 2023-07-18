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


import pandas as pd
import pm4py


# Handover of work
def handover_of_work(path_log: str, case_id_name_in_log: str, activity_name_in_log: str, resource_key: str):
    event_log = __csv_extractor_pm4py(path_log=path_log, case_id_name_in_log=case_id_name_in_log,
                                      activity_name_in_log=activity_name_in_log)
    hw_values = pm4py.discover_handover_of_work_network(event_log, resource_key=resource_key)
    return hw_values


# Subcontracting
def subcontracting(path_log: str, case_id_name_in_log: str, activity_name_in_log: str, resource_key: str):
    event_log = __csv_extractor_pm4py(path_log=path_log, case_id_name_in_log=case_id_name_in_log,
                                      activity_name_in_log=activity_name_in_log)
    subcontracting_values = pm4py.discover_working_together_network(event_log, resource_key=resource_key)
    return subcontracting_values


# Working Together
def working_together(path_log: str, case_id_name_in_log: str, activity_name_in_log: str, resource_key: str):
    event_log = __csv_extractor_pm4py(path_log=path_log, case_id_name_in_log=case_id_name_in_log,
                                      activity_name_in_log=activity_name_in_log)
    sim_activities_values = pm4py.discover_activity_based_resource_similarity(event_log, resource_key=resource_key)
    return sim_activities_values


# Similar Activities
def similar_activities(path_log: str, case_id_name_in_log: str, activity_name_in_log: str, resource_key: str):
    event_log = __csv_extractor_pm4py(path_log=path_log, case_id_name_in_log=case_id_name_in_log,
                                      activity_name_in_log=activity_name_in_log)
    working_together_values = pm4py.discover_handover_of_work_network(event_log, resource_key=resource_key)
    return working_together_values


# Take csv path as input and create a Pm4Py event log out of it.
# @private
def __csv_extractor_pm4py(path_log: str, case_id_name_in_log: str, activity_name_in_log: str):
    event_log_pm4py = pm4py.convert_to_event_log(
        pm4py.format_dataframe(df=pd.read_csv(path_log), case_id=case_id_name_in_log, activity_key=activity_name_in_log)
        , case_id_key=case_id_name_in_log)

    return event_log_pm4py
