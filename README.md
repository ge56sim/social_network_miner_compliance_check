# Social Network Mining From Natural Language Text and Event Logs for Compliance Deviation Checks 
- This repository contains the evaluation for the CoopIS 2023 submission and can be used to analyze and detect compliance deviations in traces of an event log by a ground-truth graph object from a corresponding process description.
- The repository is updated and contains the CoopIS 2023 reviews and is accepted for the conference
## Set up:
- Clone the project:
```bash
git clone https://github.com/ge56sim/org_mining_from_text.git
```
- Create conda environment based on environment.yml file:
1. Change to project directory path: **social_network_miner_compliance_check** in terminal

2. Create conda environment **snm_checker**:
```bash
conda env create -f environment.yml
```
3. After installing all dependencies successfully, activate the environment:
```bash
conda activate snm_checker
```
4. To run the own created compliance deviation checks of a dataset's SNG-T and SNG-EL:
``` 
4.1 Go to the "main_execution.py" file
4.2 Uncomment the "execute_social_network_mining_compliance_deviation_process()" method in the main method
4.3 Check the TODOS in the "execute_social_network_mining_compliance_deviation_process()" method
4.4 Add or uncomment the dataset that should be analyzed for resource interaction and compliance deviations
4.5 Change the parameters in the methods based on the activated datsets in 4.3)
4.6 Execute the main method
```
5. To run the Pm4Py: Working together and handover of work:
```
5.1 Go to the "main_execution.py" file
5.2 Uncomment the "pm4py_snm()" method
5.3 Check the TODOS and add or uncomment the datasets
5.4 Execute the main method 
```
- General:
If you encounter any issues, please reach out to the authors for assistance and guidance. Your input is invaluable in improving our work.