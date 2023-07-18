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
This file implements the class Attribute which gets as parameters a key and value
"""


# Attribute class depends on the existence of an event
class Attribute:
    def __init__(self, key: str, value) -> None:
        self.key = key
        self.value = value

    # Returns the key of the attribute: The identifier (column)
    def get_key(self) -> str:
        return self.key

    # Returns the value of the attribute: The value in row for column
    def get_value(self):
        return self.value


# Inherits Attribute -> Attributes which are always the same in the trace: case_id, ...
class CaseAttribute(Attribute):
    def __init__(self, key, value) -> None:
        super().__init__(key, value)


# Inherits Attribute -> Attributes which change for every event in trace: activity_check_one, time, resource
class EventAttribute(Attribute):
    def __init__(self, key, value) -> None:
        super().__init__(key, value)
