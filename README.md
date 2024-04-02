This repo contains the source code of experiments for ["Mining Domain-Based Policies"](https://doi.org/10.1145/3626232.3653265) paper.

You may need install the following python libraries:
1. numpy 
2. scipy 
3. disjoint-set 
4. stirling 
5. python-sat

You can install them by the following commands:
- python3.10 -m pip install --upgrade --user numpy scipy disjoint-set stirling python-sat[pblib,aiger]

The **_input_** folder contains the dataset that are used for the experiments.

The **_slurm_** folder contains the scripts to run the experiments on the ARC cluster.

The **dataset_generator.py** is used to generate random input dataset.
You can tune parameters in the **config_dataset.json**.

The **partial_specified_policy.py** contains different functions to create partial specified matries.

Given an instance of DBPM, a name of encoding and the timeout, 
the **maxsat_solver.py** is used to create different encodings and call a MaxSAT solver to solve it. 

Given the name of encoding, the directory of input instances, the directory of output and the timeout,
The **test_driver.py** traversed and solve each instance from the input directory and stored the result to the output directory.

The **data_analyzer.py** is used to analysis the output result.

The **cactus.tex** is used to draw the result in form of the Cactus plot.
