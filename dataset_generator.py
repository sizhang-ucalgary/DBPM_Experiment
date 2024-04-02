from partial_specified_policy import partial_matrix_from_summary_digraph
import numpy as np
import datetime
import logging
import json
import sys
import os



########################################################
# python3.10 dataset_generator.py config_dataset.json
########################################################
def main(argv):
    config_file = sys.argv[1]  # the config file name
    
    with open(config_file, 'r') as fp:
        config = json.load(fp)

        k = config['K#']    # the number of rights
        m = config['M#']    # the number of vertices in H
        n = config['N#']    # the number of vertices in G
        ps = config['PS%']  # the percentage of *s in G
        
        cnt = config['Instances#'] # the number of instances to generate
        path = config['Path']      # the path of folder to save instances
        prefix = config['Prefix']  # the prefix name of instances 
        
        # Create the destination folder if it doesn't exist
        os.makedirs(path, exist_ok=True)

        # add the current time and pid to the file_name
        timestamp = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S%f_')
        pid = os.getpid()
        file_name = path + '/' + prefix + str(timestamp) + str(pid)
        
        logging.basicConfig(level=logging.INFO, filename='dataset_generator.out', format='%(asctime)s - %(levelname)s - %(message)s')
        
        for i in range(1, cnt+1):
            # randomly generate H by ratio of 0s and 1s
            H = np.random.choice(['0','1'], size=(k,m,m), p=[0.5, 0.5])
            G = partial_matrix_from_summary_digraph(H, n, ps)
            # save this instance to a json file
            data = {'num_rights': k,
                    'vertex_size_in_H': m,
                    'vertex_size_in_G': n,
                    'wildcard_ratio_in_G': ps,
                    'summary_digraph': H.tolist(),
                    'partial_policy': G.tolist()}
            instance_name = file_name + str(i) + '.json'
            logging.info('Created an instance ' + instance_name)
            with open(instance_name, "w") as fp:
                json.dump(data, fp)

        logging.info('In total, created ' + str(cnt) + ' instances in the \"' + path + '\" folder.\n')



if __name__ == '__main__':
    main(sys.argv[1:])
