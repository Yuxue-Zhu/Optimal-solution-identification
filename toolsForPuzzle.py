import math
import random
import pandas as pd
import matplotlib.pyplot as plt
def getpuzzle(numberOfPlays,puzzles):
    result=[]
    puzzlesamples=[i for i in puzzles if len(puzzles[i])==numberOfPlays and puzzles[i][0]["distance"]!=float('-inf') ]
    puzzleCode=random.choice(puzzlesamples)
    for p in puzzles[puzzleCode]:
        result.append((p["score"],p["nGaps"],p["distance"]))
    return (result,puzzleCode)

def drawDistancePlot(puzzle, size):
    df=pd.DataFrame(puzzle, columns =["score","nGaps","distance"])
    best=df[df["distance"]>-3]
    false=df[df["distance"]<=-3]

    f=plt.scatter(false['score'],false['nGaps'],c=false["distance"],s=25, edgecolors="black",alpha=0.3, label='Far from pareto front')
    plt.scatter(best['score'],best['nGaps'],c=best["distance"],s=105, edgecolors="black",alpha=0.3,label='Close to pareto front')
    plt.gca().invert_yaxis()

    plt.clim(0, min(df["distance"]))
    plt.colorbar().set_label('Distance')
    plt.legend(bbox_to_anchor=(1.2, 1),loc=2, borderaxespad=0.1)
    plt.suptitle('All sollutions to the same family of puzzles by distance of size %d'%size)
    plt.xlabel('Score')
    plt.ylabel('nGaps')



def resetPareto(data):
    for puzzles in data:
        for i in data[puzzles]:
            if 'Best' in i['pareto']:
                i['pareto']='Best'
            elif 'True' in i['pareto']:
                i['pareto']='True'
            elif 'False' in i['pareto']:
                i['pareto']='False'
def classifyBypuzzles(data):
    puzzles={}
    for p in data:
        for i in data[p]:
            puzzles.setdefault(i['originalCode'],[]).append(i)
    return puzzles
def classifyByplayers(data):
    players={}
    for puzzles in data:
        for i in data[puzzles]:
            for p in i['playerIDs']:
                players.setdefault(p,[]).append(i)
    return players
def optimalPuzzles(puzzle):
    best=[]
    for i in puzzle:
        if i['pareto']=='Best':
            best.append(i)
    return best

def puzzleDistance(puzzles):
    for puzzle in puzzles:
        optimals=optimalPuzzles(puzzles[puzzle])
        for p in puzzles[puzzle]:
            if p in optimals:
                p['distance']=0.0
            else:
                minDistance=float('inf')
                for opt in optimals:
                    dist=(p['score']-opt['score'])**2+(p['nGaps']-opt['nGaps'])**2
                    if dist < minDistance :
                        minDistance=dist
                p['distance']=0.0-math.sqrt(minDistance)
def isOptimal(cutoff,puzzles):
    for puzzle in puzzles:
        for p in puzzles[puzzle]:
            if p['distance']>=cutoff:
                p['optimal']=True
            else:
                p['optimal']=False

