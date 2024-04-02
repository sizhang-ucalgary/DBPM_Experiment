import subprocess
import logging
import json
import sys
import os


########################################################
def traversal_all_files(input_dir, output_dir, method, seconds):
    data_files = []
    for dir_path, folders, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.json'):
                data_files.append(os.path.join(dir_path, file_name))
    
    # Create the destination folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    raw_file = output_dir + '/'+ method +'.json'
    
    for data_file in data_files:
        logging.info('Formulate an instance ' + data_file + ' by encoding method ' + method)
        
        # call the solver to find the solution of the problem
        program = subprocess.Popen(['python3.10', 'maxsat_solver.py', data_file, method, seconds], \
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = program.communicate()
        
        if program.returncode != 0:
            logging.info('There is an error : ' + error)
        else:        
            input_string = output.rstrip()
            result = json.loads(input_string.replace("'", "\""))
            logging.info('The solver wrote the solution to ' + raw_file + '\n')
            raw_data = {'problem': data_file, 'result': result}
            with open(raw_file, 'a') as fp:
                json.dump(raw_data, fp)
                fp.write('\n')

################################################################
# python3.10 test_driver.py method input rawdata 300
################################################################
def main(argv):
    name = sys.argv[1]         # the name of encoding method
    input_dir = sys.argv[2]    # the directory to load inputs
    output_dir = sys.argv[3]   # the directory to save outputs
    timeout = sys.argv[4]      # run the experiment with a timeout in seconds
    
    logging.basicConfig(level=logging.INFO, filename=name + '_' + input_dir.split("/")[-1] + '.out', format='%(asctime)s - %(levelname)s - %(message)s')
    
    traversal_all_files(input_dir, output_dir, name, timeout)



if __name__ == '__main__':
    main(sys.argv[1:])
