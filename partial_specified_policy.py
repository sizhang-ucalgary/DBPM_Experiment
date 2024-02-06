from disjoint_set import DisjointSet
#from stirling import k_subsets
import numpy as np
import itertools
import random
import math


########################################################
def partial_matrix_from_summary_digraph(H, n, ps):    
    k, m, _ = H.shape
    if n >= m:
        # create G
        G = np.full((k,n,n), ' ', dtype=str)
        
        # equally groups n elements into m classes
        partitions = [[j for j in range(n) if j % m == i] for i in range(m)]
        '''
        # randomly groups n elements into m classes
        partitions = random.choice(list(k_subsets(list(range(n)), m)))
        '''
        # update G based on the adjacency and non-adjacency of H
        for a in range(k):
            for u in range(m):
                for v in range(m):
                    for i in partitions[u]:
                        for j in partitions[v]:
                            if H[a,u,v] == '1':
                                G[a,i,j] = '1'
                            else:
                                G[a,i,j] = '0'
        
        # randomly change cells in G to wildcards
        total_cells = G.size
        num_wildcards = int(total_cells * ps)
        indices_to_change = np.random.choice(total_cells, num_wildcards, replace=False)
        G.flat[indices_to_change] = '*'
        #print(G)
        return G
    else:
        print('partial_matrix_from_summary : n is less than m') 


def partial_matrix_by_percent(k, n, plist):
    if math.isclose(sum(plist), 1):
        return np.random.choice(['0','1','*'], size=(k,n,n), p=plist)
    else:
        print('partial_matrix_by_percent : total percentage > 100%')


def partial_matrix_by_quantity(k, n, num_wildcards):
    total_size = k*n*n
    if total_size >= num_wildcards:
        num_non_wildcards = total_size - num_wildcards
        non_wildcards = np.random.choice(['0','1'], size=num_non_wildcards)
        wildcards = np.repeat('*', num_wildcards)
        elements = np.concatenate([non_wildcards, wildcards])
        np.random.shuffle(elements)
        partial_matrix = elements.reshape(k, n, n)
        return partial_matrix
    else:
        print('partial_matrix_by_quantity : too many wildcards')


def estimate_min_eq_classes(M):
    m = M.shape[1]
    # find the indices of the * characters in the matrix
    wildcard_indices = np.where(M=='*')
    num_wildcards = len(wildcard_indices[0])
    specified_matrix = M.copy()
    # replace the * in the matrix with each combination of 0 and 1
    for n in range(2 ** num_wildcards):
        binary = format(n, f'0{num_wildcards}b')
        idx = 0
        for k, i, j in zip(wildcard_indices[0], wildcard_indices[1], wildcard_indices[2]):
            specified_matrix[k, i, j] = binary[idx]
            idx += 1
        mi = summarize(specified_matrix)
        m = min(m, mi)
    return m


def estimate_m(M):
    M0 = np.where(M=='*', '0', M)
    M1 = np.where(M=='*', '1', M)
    m0 = summarize(M0)
    m1 = summarize(M1)
    m = min(m0, m1)
    return m


def indistinguishable(G, u, v):
    slices, rows, cols = G.shape
    if rows == cols:
        res = []
        for a in range(slices):
            one = (G[a,u,u] == '1' and G[a,u,v] == '1' and \
                   G[a,v,u] == '1' and G[a,v,v] == '1') or \
                  (G[a,u,u] == '0' and G[a,u,v] == '0' and \
                   G[a,v,u] == '0' and G[a,v,v] == '0')
            two = []
            s = set([i for i in range(rows)])
            for x in s.difference({u,v}):
                cond = (G[a,u,x] == G[a,v,x]) and (G[a,x,u] == G[a,x,v])
                two.append(cond)
            res.append(one and all(two))
        return all(res)
    else:
        print('indistinguishable : G is not k x n x n matrix')


def summarize(G):
    ds = DisjointSet()
    _, rows, cols = G.shape
    if rows == cols:
        for i in range(rows):
            ds.find(i)
        for (u,v) in itertools.combinations([i for i in range(rows)], 2):
            if (ds.find(u) != ds.find(v)) and (indistinguishable(G, u, v)):
                ds.union(u, v)
        #print(list(ds.itersets()))
        return len(list(ds.itersets()))
    else:
        print('summarize : G is not k x n x n matrix')
