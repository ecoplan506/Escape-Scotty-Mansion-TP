import random

'''Kruskal's Algorithm, Inspired by https://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm'''

class Maze:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.mazeLines = generateMaze(createEdgeSet(rows, cols))
        self.win = self.randomWinCell()

    def __repr__(self):
        return repr(self.mazeLines)

    def randomWinCell(self):
        randomBorderingCells = [(random.choice([(0, 'up'), (self.rows-1, 'down')]), random.randrange(0, self.cols)), 
                                (random.randrange(0, self.rows), random.choice([(0, 'left'), (self.cols-1, 'right')]))]
        winR, winC = random.choice(randomBorderingCells)
        if type(winR) == tuple:
            winR, direction = winR
        else:
            winC, direction = winC
        return (winR, winC, direction)

def generateMaze(edges):
    forests = {}
    mazeEdges = set()
    while len(edges) != 0:
        cell1, direction = edges.pop()
        if direction == 'down':  cell2 = (cell1[0] + 1, cell1[1])
        else:                    cell2 = (cell1[0], cell1[1] + 1)
        
        forest1 = forests.get(cell1, Forest(cell1))
        forest2 = forests.get(cell2, Forest(cell2))
        if forest1 != forest2:
            forest1.combine(forest2)
            for cell in forest2.trees:
                forests[cell] = forest1
        else: 
            #store where edges will be drawn
            row, col = cell1
            mazeEdges.add((row, col, direction))
    return mazeEdges

def createEdgeSet(rows, cols):
    edges = []
    for r in range(rows):
        for c in range(cols):
            if r < rows-1:
                edges.append(((r,c),'down'))
            if c < cols-1:
                edges.append(((r,c),'right'))
    random.shuffle(edges)
    return set(edges)

class Forest:
    count = 0
    def __init__(self, initialCell):
        self.trees = set([initialCell])
        self.id = Forest.count
        Forest.count += 1
    
    def combine(self, other):
        if type(other) == Forest:
            for cell in other.trees:
                self.trees.add(cell)
        other.trees = self.trees

    def __eq__(self, other):
        return self.id == other.id
    
    def __repr__(self):
        return str(self.id)