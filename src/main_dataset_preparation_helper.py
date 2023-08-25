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

import os

from dotenv import load_dotenv

import pandas as pd


def setup_environment():
    # Load environment variables from the .env file
    load_dotenv()
    return os.environ['HOME_PATH']


def remove_column(csv_file_name, column_names):
    # Read the CSV file
    with open(csv_file_name, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Determine the index of the column to remove
    for column_name in column_names:

        header_row = rows[0]
        column_index = header_row.index(column_name)

        # Remove the column from all rows
        for row in rows:
            del row[column_index]

    # Write the updated data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def remove_rows(csv_file_name, column_name, target_value):
    # Read the CSV file
    with open(csv_file_name, 'r') as file:
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


def rename_csv_column(csv_path, old_column_name, new_column_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Check if the old column name exists in the DataFrame
    if old_column_name not in df.columns:
        return "Error: The specified old column name does not exist in the CSV."

    # Rename the column
    df.rename(columns={old_column_name: new_column_name}, inplace=True)

    # Save the DataFrame back to the CSV file
    df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    # Helper
    # Functions that remove rows in a csv file with unwanted values and after that the whole column storing this value:
    # PermitLog, Log of BPIC20
    csv_file = '/Users/henryk/resource_compliance/snm/snm_checker_v1/data/input/log/selected/BPIC_SNG_EL_Eval/PermitLog.csv'
    column_names_first = ['case:RequestedAmount_0',
                          'case:Overspent',
                          'case:travel permit number',
                          'case:DeclarationNumber_0',
                          'case:id',
                          'case:RequestedBudget',
                          'case:BudgetNumber',
                          'case:OverspentAmount',
                          'case:dec_id_5',
                          'case:dec_id_6',
                          'case:dec_id_3',
                          'case:dec_id_4',
                          'case:dec_id_1',
                          'case:dec_id_2',
                          'case:DeclarationNumber_10',
                          'case:RequestedAmount_16',
                          'case:RequestedAmount_14',
                          'case:RequestedAmount_15',
                          'case:dec_id_9',
                          'case:RequestedAmount_12',
                          'case:DeclarationNumber_14',
                          'case:DeclarationNumber_13',
                          'case:RequestedAmount_13',
                          'case:dec_id_7',
                          'case:RequestedAmount_10',
                          'case:DeclarationNumber_12',
                          'case:dec_id_8',
                          'case:DeclarationNumber_11',
                          'case:RequestedAmount_11',
                          'case:DeclarationNumber_16',
                          'case:DeclarationNumber_15',
                          'case:DeclarationNumber_8',
                          'case:DeclarationNumber_9',
                          'case:DeclarationNumber_4',
                          'case:DeclarationNumber_5',
                          'case:DeclarationNumber_6',
                          'case:DeclarationNumber_7',
                          'case:RequestedAmount_4',
                          'case:DeclarationNumber_1',
                          'case:RequestedAmount_3',
                          'case:DeclarationNumber_2',
                          'case:RequestedAmount_2',
                          'case:RequestedAmount_1',
                          'case:DeclarationNumber_3',
                          'case:RequestedAmount_8',
                          'case:RequestedAmount_7',
                          'case:RequestedAmount_6',
                          'case:RequestedAmount_5',
                          'case:RequestedAmount_9',
                          'case:dec_id_16',
                          'case:dec_id_13',
                          'case:dec_id_12',
                          'case:dec_id_15',
                          'case:dec_id_14',
                          'case:dec_id_11',
                          'case:dec_id_10',
                          'case:Activity_1',
                          'case:Activity_0',
                          'case:RfpNumber_0',
                          'case:OrganizationalEntity_0',
                          'case:Rfp_id_0',
                          'case:RfpNumber_1',
                          'case:OrganizationalEntity_1',
                          'case:Cost Type_1',
                          'case:Cost Type_0',
                          'case:Task_1',
                          'case:Task_0',
                          'case:Project_0',
                          'case:Rfp_id_1',
                          'case:Project_1',
                          'case:Activity_3',
                          'case:Activity_2',
                          'case:Cost Type_3',
                          'case:Cost Type_2',
                          'case:RfpNumber_2',
                          'case:RfpNumber_3',
                          'case:OrganizationalEntity_2',
                          'case:OrganizationalEntity_3',
                          'case:Project_2',
                          'case:Project_3',
                          'case:Rfp_id_3',
                          'case:Rfp_id_2',
                          'case:Task_3',
                          'case:Task_2',
                          'case:Rfp_id_10',
                          'case:Rfp_id_11',
                          'case:Rfp_id_12',
                          'case:Rfp_id_13',
                          'case:Rfp_id_14',
                          'case:Project_11',
                          'case:Project_12',
                          'case:Project_10',
                          'case:Project_13',
                          'case:Project_14',
                          'case:Cost Type_7',
                          'case:Cost Type_6',
                          'case:Cost Type_9',
                          'case:Cost Type_8',
                          'case:Cost Type_5',
                          'case:Cost Type_4',
                          'case:OrganizationalEntity_8',
                          'case:OrganizationalEntity_9',
                          'case:Task_10',
                          'case:OrganizationalEntity_6',
                          'case:Task_11',
                          'case:OrganizationalEntity_7',
                          'case:Task_12',
                          'case:Task_13',
                          'case:Task_14',
                          'case:RfpNumber_10',
                          'case:RfpNumber_12',
                          'case:RfpNumber_11',
                          'case:OrganizationalEntity_4',
                          'case:Project_6',
                          'case:RfpNumber_14',
                          'case:OrganizationalEntity_5',
                          'case:Project_7',
                          'case:RfpNumber_13',
                          'case:Project_8',
                          'case:Project_9',
                          'case:Project_4',
                          'case:Project_5',
                          'case:Activity_12',
                          'case:Activity_11',
                          'case:Activity_14',
                          'case:Activity_13',
                          'case:Activity_10',
                          'case:OrganizationalEntity_14',
                          'case:OrganizationalEntity_13',
                          'case:RfpNumber_8',
                          'case:RfpNumber_9',
                          'case:RfpNumber_6',
                          'case:RfpNumber_7',
                          'case:RfpNumber_4',
                          'case:RfpNumber_5',
                          'case:OrganizationalEntity_12',
                          'case:OrganizationalEntity_11',
                          'case:OrganizationalEntity_10',
                          'case:Rfp_id_7',
                          'case:Rfp_id_8',
                          'case:Rfp_id_5',
                          'case:Rfp_id_6',
                          'case:Rfp_id_4',
                          'case:Rfp_id_9',
                          'case:Activity_9',
                          'case:Activity_8',
                          'case:Activity_5',
                          'case:Activity_4',
                          'case:Activity_7',
                          'case:Activity_6',
                          'case:Cost Type_13',
                          'case:Cost Type_14',
                          'case:Cost Type_10',
                          'case:Cost Type_11',
                          'case:Cost Type_12',
                          'case:Task_5',
                          'case:Task_4',
                          'case:Task_9',
                          'case:Task_8',
                          'case:Task_7',
                          'case:Task_6'
                          ]

    column_names_second = ['concept:instance', 'case:OrganizationalEntity', 'case:ProjectNumber', 'case:ActivityNumber', 'case:TotalDeclared']

    column_names_third = ['case:TaskNumber']

    # Remove unnecessary columns
    # remove_column(csv_file_name=csv_file, column_names=column_names_third)

    # Removed all rows where org:role == MISSING, UNDEFINED, PRE_APPROVER
    # remove_rows(csv_file_name=csv_file, column_name='org:role', target_value='PRE_APPROVER')

    # rename_csv_column(csv_path=csv_file, old_column_name='case:concept:name', new_column_name='concept:instance')

