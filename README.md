# Social Network Mining From Natural Language Text and Event Logs for Compliance Deviation Checks 
This repository contains the evaluation for the CopIS 2023 submission and can be used to analyze and detect compliance deviations in traces of an event log by a ground-truth graph object from a corresponding process description.

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
conda activate org_mining
```
4. To run the project:
```
4.1 add all necessary inputs in the config file
4.2 execute in the src/main_execution the process method
```

If you encounter any issues, please reach out to the authors for assistance and guidance. Your input is invaluable in improving our work.