import main
import const
import pygame
import numpy as np

def solve(start,end,drawingGrid,window,clock):

    startNode = None
    endNode = None
    grid = [[None for i in range(const.TILE_NB)] for j in range(const.TILE_NB)]
    for x in range(len(drawingGrid)):
        for y in range(len(drawingGrid[x])):
            walkable = not bool(drawingGrid[x][y])
            grid[x][y] = Node(walkable,x,y)
            if start == (x,y): startNode = grid[x][y]
            if end == (x,y): endNode = grid[x][y]

    openSet = [startNode]
    closedSet = []

    while len(openSet) > 0:
        # Rendering stuff
        if (const.SOLVING_FPS != -1):
            clock.tick(const.SOLVING_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Algorithm
        currentNode = openSet[0]
        for i in range(1,len(openSet)):
            if openSet[i].fCost() < currentNode.fCost() or (openSet[i].fCost() == currentNode.fCost() and openSet[i].hCost < currentNode.hCost):
                currentNode = openSet[i]

        openSet.remove(currentNode)
        closedSet.append(currentNode)
        drawingGrid[currentNode.x][currentNode.y] = 3

        if (currentNode == endNode):
            # Finished
            RetracePath(startNode,endNode, drawingGrid, clock, window, start, end)
            return

        for neighbour in getNeighbours(currentNode, grid):
            if not neighbour.walkable or neighbour in closedSet:
                continue

            newMovementCostToNeighbour = currentNode.gCost + getDistance(currentNode, neighbour)
            if newMovementCostToNeighbour < neighbour.gCost or (not neighbour in openSet):
                
                neighbour.gCost = newMovementCostToNeighbour
                neighbour.hCost = getDistance(neighbour, endNode)
                neighbour.parent = currentNode

                if not neighbour in openSet:
                    openSet.append(neighbour)
                    drawingGrid[neighbour.x][neighbour.y] = 2



        # Rendering stuff
        main.draw_window(window, drawingGrid, start, end)

def RetracePath(startNode, endNode, drawingGrid, clock, window, start, end):
    path = []
    currentNode = endNode

    while currentNode != startNode:

        # Rendering stuff
        if (const.SOLVING_FPS != -1):
            clock.tick(const.SOLVING_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        drawingGrid[currentNode.x][currentNode.y] = 4
        path.append(currentNode)
        currentNode = currentNode.parent

        main.draw_window(window, drawingGrid, start, end)


def getNeighbours(node, grid):
    neighbours = []
    
    # Loop from -1 to 1
    for x in range(-1,2):
        for y in range(-1,2):
            if x == 0 and y == 0:
                continue
            
            checkX = node.x + x
            checkY = node.y + y

            if(checkX >= 0 and checkX < len(grid) and checkY >= 0 and checkY < len(grid[0])):
                neighbours.append(grid[checkX][checkY])

    return neighbours


def getDistance(nodeA, nodeB):
    dstX = abs(nodeA.x - nodeB.x)
    dstY = abs(nodeA.y - nodeB.y)

    if dstX > dstY:
        return 14*dstY + 10*(dstX-dstY)
    else:
        return 14*dstX + 10*(dstY-dstX)


class Node():
    def __init__(self, walkable, x, y):
        self.walkable = walkable
        self.x = x
        self.y = y
        self.gCost = 0
        self.hCost = None
        self.parent = None

    def fCost(self):
        return self.gCost + self. hCost