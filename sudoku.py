#!/usr/bin/env python3

import numpy as np
import os
import itertools
import sys

intro = """
This program will solve sudoku 9x9 for you
Usage: sudoku.py filename

filename must contain sudoku in the following format:
8********
**36*****
*7**9*2**
*5***7***
****457**
***1***3*
**1****68
**85***1*
*9****4**

Example:
    sudoku.py sudoku
"""

if len(sys.argv) == 1:
    print(intro)
    exit(0)
elif len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        ar = f.read().split('\n')
else:
    print("Wrong argument number")
    exit(-1)

clauses = []

digits = range(1,10)

def varnum(i,j,k):
    assert (i in digits and j in digits and k in digits)
    return i*100+j*10+k

def exactly_one_of(literals):
    clauses.append([l for l in literals])

    for pair in itertools.combinations(literals,2):
        clauses.append([-l for l in pair])

for (i,j) in itertools.product(digits,repeat=2):
    exactly_one_of([varnum(i,j,k) for k in digits])
    
for (i,k) in itertools.product(digits,repeat=2):
    exactly_one_of([varnum(i,j,k) for j in digits])

for (j,k) in itertools.product(digits,repeat=2):
    exactly_one_of([varnum(i,j,k) for i in digits])

for t in range(3):
    for u in range(3):
        x = t*3+1
        y = u*3+1
        for k in digits:
            lst = []
            lst2 = []
            for i in range(3):
                for j in range(3):
                    lst.append(varnum(x+i,y+j,k))
                    lst2.append((x+i,y+j,k))
            exactly_one_of(lst)
            #print(lst)
            #print(lst2)
    
for i in range(len(ar)):
    for j in range(len(ar[i])):
        if (ar[i][j] != '*'):
            #print(i,j,int(ar[i][j]))
            clauses.append([varnum(i+1,j+1,int(ar[i][j]))])

with open("code_2_formula.cnf","w") as f:
    f.write("p cnf {} {}\n".format(1000,len(clauses)))
    for c in clauses:
        c.append(0)
        f.write(" ".join(map(str,c))+'\n')

os.system("minisat code_2_formula.cnf code_2_ans.cnf")

ans = []
with open("code_2_ans.cnf","r") as r:
    s = r.readline()
    ar = [int(i) for i in ((r.readline()).split(' ')[:-1])]
    #print(ar)
    k = 0
    for i in range(len(ar)):
        if (ar[i]>0):
            print(ar[i]%10,end=' ')
            k+=1
            if (k == 9):
                print('')
                k=0
