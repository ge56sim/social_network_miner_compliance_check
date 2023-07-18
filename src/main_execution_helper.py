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
This file is a main file that can be executed but only provides functionality to create gold standard evaluation data
or provides functions that maintain the output data.
"""

import csv


def remove_rows_and_column(csv_file, column_name, target_value):
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Remove rows with the target value in the specified field
    filtered_rows = [row for row in rows if row[column_name] != target_value]

    # Write the updated data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in filtered_rows:
            writer.writerow(row)


def remove_column_by_name(csv_file, column_name):
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Determine the index of the column to remove
    header_row = rows[0]
    column_index = header_row.index(column_name)

    # Remove the column from all rows
    for row in rows:
        del row[column_index]

    # Write the updated data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


if __name__ == "__main__":
    None
    # Helper
    # Functions that remove rows in a csv file with unwanted values and after that the whole column storing this value:

    # csv_file = '/Users/henryk/Guided_Research_SS2023/org_mining_from_text/data/input/log/selected/SM_event_log.csv'
    # column_name = 'lifecycle:transition'
    # target_value = 'done'

    # remove_rows_and_column(csv_file, column_name, target_value)
    # remove_column_by_name(csv_file, 'org:org')
