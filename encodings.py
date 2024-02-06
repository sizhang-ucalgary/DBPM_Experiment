#from partial_specified_policy import estimate_m
from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2

import numpy as np
import logging
import signal
import time
import math
import json
import sys
import os

########################################################

def solve(problem):
    # Solve the MaxSAT model by using RC2 algorithm
    with RC2(problem) as solver:
        sol = solver.compute()
        if sol == None:
            return 'UNSATISFIABLE'
        else:
            return str(solver.cost)

def handle_timeout(sig, frame):
    raise TimeoutError('RC2 Solver timed out.')

########################################################

def formulate(M, m, method):
    formula = WCNF()
    rights, vertices, _ = M.shape
    eqclasses = m
    counter = 1
    
    # Define Boolean Variables
    x = np.arange(rights*vertices*vertices).\
        reshape(rights,vertices,vertices) + counter
    counter += x.size

    y = np.arange(vertices*eqclasses).\
        reshape(vertices,eqclasses) + counter
    counter += y.size

    z = np.arange(rights*eqclasses*eqclasses).\
        reshape(rights,eqclasses,eqclasses) + counter
    counter += z.size

    r = np.arange(eqclasses) + counter
    counter += r.size
    
    if method == 'BE_NF_FM' or method == 'BE_NF_MD' or method == 'BE_NF_MD_LI':
        l = np.arange(vertices*eqclasses).\
            reshape(vertices,eqclasses) + counter
        counter += l.size
    
    # Define Hard Clauses
    if method == 'BE_CC':
        # Cardinality Constraint - ladder encoding
        vpool = IDPool(occupied=[[1, counter]])
        for i in range(vertices):
            formula.extend(CardEnc.equals(lits=y[i,:].tolist(), bound=1, vpool=vpool, encoding=EncType.ladder))
    else:
        # f has at least one image
        for i in range(vertices):
            formula.append(y[i,:].tolist())
            
        if method == 'BE':
            # f is a function - at most one image
            for i in range(vertices):
                for p in range(eqclasses):
                    for q in range(eqclasses):
                        if p < q:
                            formula.append([ -y[i,p].item(), -y[i,q].item() ])

    # f is a strong homomorphism
    for t in range(rights):
        for i in range(vertices):
            for j in range(vertices):
                for p in range(eqclasses):
                    for q in range(eqclasses):
                        if M[t,i,j] == '0':
                            formula.append([ -y[i,p].item(), -y[j,q].item(), -z[t,p,q].item() ])
                        elif M[t,i,j] == '1':
                            formula.append([ -y[i,p].item(), -y[j,q].item(),  z[t,p,q].item() ])
                        else:
                            formula.append([ -y[i,p].item(), -y[j,q].item(),  x[t,i,j].item(), -z[t,p,q].item() ])
                            formula.append([ -y[i,p].item(), -y[j,q].item(), -x[t,i,j].item(),  z[t,p,q].item() ])

    # Identify non-empty classes
    for i in range(vertices):
        for p in range(eqclasses):
            formula.append([ -y[i,p].item(), r[p].item() ])

    if method == 'BE_NF_FM' or method == 'BE_NF_MD' or method == 'BE_NF_MD_LI':
        # Mins are sorted
        for p in range(eqclasses):
            for q in range(eqclasses):
                if p < q:
                    for i in range(vertices):
                        for j in range(vertices):
                            if i >= j:
                                formula.append([ -l[i,p].item(), -l[j,q].item() ])

        # Min is minimum
        for i in range(vertices):
            for j in range(vertices):
                if i < j:
                    for p in range(eqclasses):
                        formula.append([ -y[i,p].item(), -l[j,p].item() ])

        # Min is selected
        for i in range(vertices):
            for p in range(eqclasses):
                formula.append([ -l[i,p].item(),  y[i,p].item() ])

    if method == 'BE_NF_FM':
        # Feasible mins
        for i in range(vertices):
            for p in range(eqclasses):
                formula.append([ -y[i,p].item() ] + l[:,p].tolist())

    if method == 'BE_NF_MD' or method == 'BE_NF_MD_LI':
        # Min domain
        for p in range(eqclasses):
            formula.append([ -r[p].item() ] + l[:,p].tolist())

    if method == 'BE_NF_LI' or method == 'BE_NF_MD_LI':
        # Prefer lower-indexed classes.
        for p in range(eqclasses-1):
            formula.append([ r[p].item(), -r[p+1].item() ])

    # Define Soft Clauses
    for p in range(eqclasses):
        formula.append([ -r[p].item() ], weight=1)

    return formula

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
        with open(data_file, 'r') as fp:
            instance = json.load(fp)

        M = np.array(instance['partial_policy'])
        m = 2*int(instance['vertex_size_in_H'])

        logging.info('Formulate an instance ' + data_file + ' by encoding method ' + method)
        problem = formulate(M, m, method)

        logging.info('The solver is running.')
        # Register the signal function handler
        signal.signal(signal.SIGALRM, handle_timeout)
        # Define a timeout for your function
        signal.alarm(seconds)        
        try:
            start_time = time.time()
            sol = solve(problem)
            end_time = time.time()
            run_time = end_time - start_time
            result = {'solution': sol, 'runtime': '%0.*f' % (2, run_time)}
        except TimeoutError:
            result = {'solution': 'TIMEOUT', 'runtime': '%0.*f' % (2, seconds)}
        # Cancel the timer if the function returned before timeout
        signal.alarm(0)
        
        logging.info('The solver wrote the solution to ' + raw_file)
        raw_data = {'problem': data_file, 'result': result}
        with open(raw_file, 'a') as fp:
            json.dump(raw_data, fp)
            fp.write('\n')

################################################################
# python3.10 encodings.py method input rawdata 300
################################################################
def main(argv):
    name = sys.argv[1]              # the name of encoding method
    input_dir = sys.argv[2]         # the directory to load inputs
    output_dir = sys.argv[3]        # the directory to save outputs
    timeout = int(sys.argv[4])      # run the experiment with a timeout in seconds
    
    pid = os.getpid()
    logging.basicConfig(level=logging.INFO, filename='encodings_' + name + '_' + str(pid) +'.out', format='%(asctime)s - %(levelname)s - %(message)s')
    
    traversal_all_files(input_dir, output_dir, name, timeout)



if __name__ == '__main__':
    main(sys.argv[1:])
