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
This file consists of the class EventLog which requires as Parameter a List of Traces

The class implements several functions which provide insights of the current process log
and therefore for the real process executions
"""

# Required Imports:
from typing import List, Union, Any

# Imported class
from .trace import Trace


# Object-oriented structure of the XES Document UML Model for Event Logs
class EventLog:

    def __init__(self, traces: List[Trace]) -> None:
        self.traces = traces

    def get_network_output_of_distinct_traces_in_event_log(self, resource_structure_type: str) -> list[dict[str, Union[int, dict[Any, list[str]]]]]:
        # All Distinct Traces in the format: (list of case ids, Trace)
        distinct_trace_list = self.__get_distinct_traces(resource_structure_type=resource_structure_type)
        # Output
        output_list = []
        # Id
        distinct_trace_id = 1
        # Iterate through distinct traces
        for distinct_trace in distinct_trace_list:
            # All case ids of this trace
            case_ids = distinct_trace[0]
            # events in the trace
            event_list = distinct_trace[1].get_events_of_trace()
            # The network list filled for each trace
            network_list = []
            # Create structure of resource performer, resource consumer, activity name
            count_consumer = 1
            for event in event_list:
                # resource_performer = event['Organizational_Unit']
                resource_performer = event[resource_structure_type]
                activity = event['Activity']
                # Consumer = resource of next activity
                if count_consumer < len(event_list):
                    # resource_consumer = event_list[count_consumer]['Organizational_Unit']
                    resource_consumer = event_list[count_consumer][resource_structure_type]
                else:
                    resource_consumer = ""
                # Add infos of event to network list for trace
                network_list.append({"Resource Performer": resource_performer,
                                     "Resource Consumer": resource_consumer,
                                     "Activity": activity})
                # Increase counter to get the resource consumer
                count_consumer = count_consumer + 1
            # Add values to output for distinct trace
            output_list.append({'id': distinct_trace_id, 'case_ids': case_ids, 'network_trace': network_list})
            # Increase the output id for networks of distinct traces
            distinct_trace_id = distinct_trace_id + 1
        # Return output
        return output_list

    # Helper method to get all distinct traces in the log
    # @private
    # A distinct trace in that case is defined as a unique list of resource activity pairs
    def __get_distinct_traces(self, resource_structure_type: str) -> list:
        distinct_traces = []
        # Iterate through the traces of the event log
        for trace in self.traces:
            # Dict that stores as key the case id = as value a list of all events
            trace_structure_dict_list = trace.get_resource_activity_organisation_structure_pairs_of_trace().items()
            # Get case_id, events pair of new trace which needs to be checked
            for case_id, events in trace_structure_dict_list:
                # new distinct trace list is empty: Insert first case id as list of case ids and trace in list
                if len(distinct_traces) == 0:
                    trace_distinct = ([case_id], Trace(case_id=case_id, events=events))
                    distinct_traces.append(trace_distinct)
                # new distinct trace list is not empty: Iterate through new distinct trace list
                else:
                    # Boolean that indicates if a distinct trace is found (True),
                    # else the case id is added to the same trace(False)
                    distinct_trace_found = True
                    # Counter: important to add a case_id to the list
                    count = 0
                    # Iterate through the new list of distinct traces
                    for case_id_list, distinct_trace in distinct_traces:
                        # Distinct events
                        events_distinct = distinct_trace.get_events_of_trace()
                        # Check the list of event_ids
                        event_id_list = [event[resource_structure_type] + " " + event['Activity'] for event in events]
                        event_id_list_distinct = [distinct_event[resource_structure_type] + " " + distinct_event['Activity'] for distinct_event in events_distinct]

                        # If event is already in new distinct trace list
                        if event_id_list == event_id_list_distinct:
                            # No distinct trace was found
                            distinct_trace_found = False
                            # Add only the case id of the trace to the new list of distinct traces to the list
                            distinct_traces[count][0].append(case_id)
                        # Increase count
                        count = count + 1
                    # Add case id and trace to distinct trace, because trace could not be found in distinct traces
                    if distinct_trace_found:
                        trace = ([case_id], Trace(case_id=case_id, events=events))
                        distinct_traces.append(trace)
        # Return the list of distinct traces
        return distinct_traces
