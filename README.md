This repo contains the source code of experiments for ["Mining Domain-Based Policies"](https://doi.org/10.1145/3626232.3653265) paper.

You need install the following python libraries:
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

The **partial_specified_policy.py** contains different functions to create partial specified matrices.

Given an instance of DBPM, a name of encoding and the timeout, 
the **maxsat_solver.py** is used to create different encodings and call a MaxSAT solver to solve it. 

Given the name of encoding, the directory of input instances, the directory of output and the timeout,
The **test_driver.py** solved each instance from the input directory and saved the result to the output directory.

The **data_analyzer.py** is used to analysis the output result.

The **cactus.tex** is used to draw the result in form of the Cactus plot.

## 📖 Citation
If you use this work in your research, please cite:
```bibtex
@inproceedings{DBLP:conf/codaspy/ZhangF24,
  author       = {Si Zhang and
                  Philip W. L. Fong},
  editor       = {Jo{\~{a}}o P. Vilela and
                  Haya Schulmann and
                  Ninghui Li},
  title        = {Mining Domain-Based Policies},
  booktitle    = {Proceedings of the Fourteenth {ACM} Conference on Data and Application
                  Security and Privacy, {CODASPY} 2024, Porto, Portugal, June 19-21,
                  2024},
  pages        = {403--414},
  publisher    = {{ACM}},
  year         = {2024},
  url          = {https://doi.org/10.1145/3626232.3653265},
  doi          = {10.1145/3626232.3653265}
}
```
