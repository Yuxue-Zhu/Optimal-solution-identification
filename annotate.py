import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd
import numpy as np
import math
import progressbar
import time, sys
from scipy.optimize import fmin_cobyla
from dnapuzzle import Puzzle
import random
from toolsForPuzzle import *
from sympy import *
#estimate parameters
def paretpFront(puzzle):
    df=pd.DataFrame(puzzle, columns =["score","nGaps","distance"])
    y1=df['nGaps'].min()
    x1=df[df['nGaps']==y1]['score'].max()
    x3=df['score'].max()
    y3=df[df['score']==x3]['nGaps'].min()
    l=list(df[df['nGaps']<=y3]['nGaps'].unique())
    l.sort()
    y2=l[(len(l)-1)//2]
    x2=df[df['nGaps']==y2]['score'].max()

    a,b,c = symbols('a b c')
    return solve([Eq(a*x1**2+b*x1+c, y1), Eq(a*x2**2+b*x2+c, y2),Eq(a*x3**2+b*x3+c, y3)], [a,b,c])
def main():
    infile = open('1M_solutions_nov15.pickle','rb')
    data = pickle.load(infile)
    infile.close()
    resetPareto(data)
    puzzles=classifyBypuzzles(data)
    puzzleDistance(puzzles)
    isOptimal(-3, puzzles)
    keys=list(puzzles.keys())
    
    counter=0
    progress = progressbar.ProgressBar()
    a,b,c = symbols('a b c')
    for i in progress(keys):
            counter+=1
            puzzle = puzzles[i]
            result=[]
            maxScore=float('-inf')
            minScore=float('inf')
            for p in puzzle:
                if p["score"]>maxScore:
                    maxScore=p["score"]
                if p["score"]<minScore:
                    minScore=p["score"]
                result.append((p["score"],p["nGaps"],p["distance"]))
            ans=paretpFront(result)

            if len(ans)!=3:
                continue
            for p in puzzle:

                def f(x):

                    return ans[a]*x**2+ans[b]*x+ans[c]

                def distance(X):
                    x,y = X
                    return np.sqrt((x - p['score'])**2 + (y - p['nGaps'])**2)

                def c1(X):
                    x,y = X
                    return f(x)-y
                def c2(X):
                    x,y = X
                    return y-f(x)
                #calculate shortest distance to pareto frontier
                X = fmin_cobyla(distance, x0=[minScore,maxScore], cons=[c2,c1],rhobeg=10,rhoend=0.5, maxfun=20)
                p['paretoDist']=distance(X)
    pickle.dump( puzzles, open( "Nov_data_distance_annotated.pickle", "wb" ) )
if __name__ == '__main__':
    main()
