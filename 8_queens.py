#!/usr/bin/env python3

import numpy as np
import os

import itertools as it

intro = """
This simple program will solve 8 queens puzzle:
Place 8 queens on the chessboard so that no 2 queens threaten each other

This program supports solving n queens puzzle

Enter n: """

n = int(input(intro));

clauses = []

def varnum(i, j):
    assert (i in range(n) and j in range(n))
    return i*n+j+1

for i in range(n):
    clauses.append([varnum(i,j) for j in range(n)])
    
for i in range(n):
    for (j1,j2) in it.combinations(range(n),2):
        clauses.append([-varnum(i,j1),-varnum(i,j2)]);

for j in range(n):
    for (i1,i2) in it.combinations(range(n),2):
        clauses.append([-varnum(i1,j),-varnum(i2,j)]);

for (i1,i2) in it.combinations(range(n),2):
    assert (i1 < i2)
    for (j1,j2) in it.product(range(n),repeat = 2):
        if (i2-i1 == abs(j2-j1)):
            clauses.append([-varnum(i1,j1),-varnum(i2,j2)]);

with open("code_1_formula.cnf","w") as f:
    f.write("p cnf {} {}\n".format(n*n,len(clauses)));
    for c in clauses:
        c.append(0);
        f.write(" ".join(map(str,c))+'\n')

os.system("minisat code_1_formula.cnf code_1_ans.cnf");

with open("code_1_ans.cnf","r") as r:
    s = r.readline();
    ar = [int(i) for i in ((r.readline()).split(' ')[:-1])];
    for i in range(0,len(ar)):
        if ar[i] < 0:
            print("0 ",end='');
        elif ar[i] > 0:
            print("1 ",end='');
        if (i%n==n-1):
            print('\n')
