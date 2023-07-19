# Social Network Mining From Natural Language Text and Event Logs for Compliance Deviation Checks 
This repository contains the evaluation for the CoopIS 2023 submission and can be used to analyze and detect compliance deviations in trace graphs.
The trace graphs represent the interaction and communication traffic between resources and are checked against a ground truth graph object from a corresponding process description.

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
4. To run the project:
```
4.1 Create a .env file in the main directory and add your personal home path, e.g., /Users/Max/social_network_miner_compliance_check'
4.2 Add all necessary inputs as mentioned in the todos in the main_execution file. All data given in the data folder are already added there.
--> Currently all data is active for the Bicycle Manufacturing Dataset (BM).
--> New data cona be added by place then in the appropriate data folder and need only be added in the main_execution file.
4.3 Execute in the src/main_execution the method:' execute_social_network_mining_compliance_deviation_process()'
```

If you encounter any issues, please reach out to the authors for assistance and guidance. Your input is invaluable in improving our work.