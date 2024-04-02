from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2

import numpy as np
import signal
import time
import math
import json
import sys
import os
import gc


########################################################

def handle_timeout(sig, frame):
    raise TimeoutError('RC2 Solver timed out.')

################################################################
# python3.10 maxsat_solver.py data_file method 300
################################################################
def main(argv):
    data_file = sys.argv[1]         # the input file
    method = sys.argv[2]            # the name of encoding method
    seconds = int(sys.argv[3])      # run the solver with a timeout in seconds
    
    with open(data_file, 'r') as fp:
        instance = json.load(fp)
        M = np.array(instance['partial_policy'])
        m = 2*int(instance['vertex_size_in_H'])
        
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

        del M, x, y, z, r
        if method == 'BE_NF_FM' or method == 'BE_NF_MD' or method == 'BE_NF_MD_LI':
            del l
        gc.collect()

        # Register the signal function handler
        signal.signal(signal.SIGALRM, handle_timeout)
        # Define a timeout for your function
        signal.alarm(seconds)
    
        result = {'solution': 'UNSATISFIABLE', 'runtime': '%0.*f' % (2, seconds)} 
        # Solve the MaxSAT model by using RC2 algorithm
        try:
            with RC2(formula) as solver:
                start_time = time.time()
                solver.compute()
                end_time = time.time()
                run_time = end_time - start_time
                result = {'solution': str(solver.cost), 'runtime': '%0.*f' % (2, run_time)}
        except TimeoutError:
            result = {'solution': 'TIMEOUT', 'runtime': '%0.*f' % (2, seconds)}
        finally:
            # Reset the alarm (cancel the timeout)
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            print(result)



if __name__ == '__main__':
    main(sys.argv[1:])
