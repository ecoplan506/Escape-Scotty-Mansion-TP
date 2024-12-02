import sys
import pprint

class Maze:
    def __init__(self, rows, cols):
        edges = set()
        for r in range(rows):
            for c in range(cols):
                if r < rows-1:
                    edges.add(((r,c),(r+1,c)))
                if c < cols-1:
                    edges.add(((r,c),(r,c+1)))
        forests = {}
        self.mazeEdges = set()
       
        while len(self.edges) != 0:
            cell1 , cell2 = self.edges.pop()
            forest1 = forests.get(cell1, set(cell1)) 
            forest2 = forests.get(cell2, set(cell2))
            if forest1 != forest2:
                newForest = forest1 | forest2
                forests[cell1] = forests[cell2] = newForest
            else: 
                #store where edges will be drawn#
                self.mazeEdges = (max(cell1[0],cell2[0]), max(cell1[1],cell2[1]))

            





    def __repr__(self):
        return str(self.mazeEdges)

print(Maze(3, 3))
pprint.pprint([['False' for _ in range(3)] for _ in range(3)])