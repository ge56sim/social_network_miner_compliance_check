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
This file implements the class Event which gets as a parameter a list of Attributes
The class Event implements a function that returns wich ressource performed what activity_check_one
"""
# Imports
from typing import List, Any

# Imported class
from .attribute import Attribute


# Event Class depends on the existence of a Trace
class Event:

    def __init__(self, attribs: List[Attribute]) -> None:
        self.attribs = attribs

    def get_attributes(self) -> List[Attribute]:
        return self.attribs

    # Returns the: Resource, Activity, User, Organizational_Unit, Organization for this event
    def get_resource_activity_organisation_structure_pair(self) -> dict[str, Any]:
        res_act_org_pair = {}
        for attribute in self.attribs:
            # Id
            if attribute.get_key() == "concept:event":
                res_act_org_pair["event_id"] = attribute.get_value()
            # Execution data
            if attribute.get_key() == "concept:name":
                res_act_org_pair["Activity"] = attribute.get_value()
            if attribute.get_key() == "time:timestamp":
                res_act_org_pair["Timestamp"] = attribute.get_value()
            if attribute.get_key() == "lifecycle:transition":
                res_act_org_pair["Lifecycle_Transition"] = attribute.get_value()

                # Organisational Structure
            if attribute.get_key() == "org:resource":
                res_act_org_pair["Resource"] = attribute.get_value()
            if attribute.get_key() == "org:role":
                res_act_org_pair["Role"] = attribute.get_value()
            if attribute.get_key() == "org:unit":
                res_act_org_pair["Organizational_Unit"] = attribute.get_value()
            if attribute.get_key() == "org:org":
                res_act_org_pair["Organization"] = attribute.get_value()

        return res_act_org_pair

    # Get the resource and activity pair from the log
    def get_resource_activity_pair(self):
        res_act_pair = ()
        for a in self.attribs:
            if a.get_key() == "org:unit":
                res_act_pair = (a.get_value(),) + res_act_pair
            if a.get_key() == "concept:name":
                res_act_pair = res_act_pair + (a.get_value(),)
        return res_act_pair
