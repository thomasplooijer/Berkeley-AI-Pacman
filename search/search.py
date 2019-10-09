# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:


    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    """
    startingPos = problem.getStartState()   #verkrijg startpositie van het zoekprobleem

    if problem.isGoalState(startingPos):    #check of startpositie de goal is, zo ja stop programma
        return []                           #return an empty list

    myStack = util.Stack()                  #create stack to store nodes (function used from util.py)
    visited = []                         #create list for visited values

    myStack.push((startingPos, []))      #push startpos as single argument into stack
    while not myStack.isEmpty():
        currentPos, actions = myStack.pop()  #pop the stack
        if currentPos not in visited:
            visited.append(currentPos)

            if problem.isGoalState(currentPos):
                return actions              #return pacman path

            for successor, action, cost in problem.getSuccessors(currentPos):
                nextStep = actions + [action]               #[action] is looping through all action values
                myStack.push((successor, nextStep))        #passes 2 arguments as 1 argument. Pushes it in individually
    """
    #Every node remembers the path represented by directions
    #For example, ([10, 10], ['South', 'North', 'West', 'West', ...]

    startingPos = problem.getStartState()   #get startpositie
    myStack = util.Stack()                  #stack for pushing/popping
    visited = []                            #visited positions

    if problem.isGoalState(startingPos):
        return []      #return empty list, stops script

    myStack.push((startingPos, []))  # push startpos as node and empty direction into stack
    while not myStack.isEmpty():
        # popping puts 1st argument node in currentPos, and 2nd argument path in path
        currentPos, path = myStack.pop()

        if currentPos not in visited:
            visited.append(currentPos)

            if problem.isGoalState(currentPos):
                return path     #path is directions (n,w,s,e etc)

            for successors, directions, cost in problem.getSuccessors(currentPos):
                nextPos = path + [directions]
                myStack.push((successors, nextPos))   #push successlocations and full path into stack


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    myQueue = util.Queue()
    visited = []

    #at question 5 startingPos becomes a list of [(startingPosition), (corners)]
    startingPos = problem.getStartState()
    #print startingPos

    if problem.isGoalState(startingPos):
        return []

    myQueue.push((startingPos, []))     #push in starting location (startingPos, []) and empty list, pass 2 as 1 because self is passed too = 2 arguments
    while not myQueue.isEmpty():
        node, path = myQueue.pop()     #check first element of queue, first in first out

        if node not in visited:
            visited.append(node)

            #node found at (6, 6), goal is found, path is returned NOT GOOD
            if problem.isGoalState(node):
                return path     #return full path if goal is found

            for successornodes, actions, cost in problem.getSuccessors(node):
                addPath = path + [actions]      #add actions to existing path addpath = [path, actions]
                myQueue.push((successornodes, addPath)) #path stays intact throughout whole scipt


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    """
    myQueue = util.PriorityQueue()
    visited = []

    startPos = problem.getStartState()
    node = (startPos, [], 0)

    if problem.isGoalState(startPos):
        return []

    myQueue.push(node, 0)     #push in starting location, empty list for actions, and 0 for priority (not used yet)
    while not myQueue.isEmpty():
        #data[], startPos, 0 = path, 1 = priority
        node = myQueue.pop()     #check first element of queue, first in first out

        if node[0] not in visited:
            visited.append(node[0])

            if problem.isGoalState(startPos):
                return node[1]     #return full path if goal is found

            for successornodes, actions, cost in problem.getSuccessors(node[0]):
                #needs work
                addPath = node[1] + [actions]      #add actions to existing path addpath = [path, actions]
                myQueue.push((successornodes, addPath, newPriority), newPriority) #path stays intact throughout whole scipt
    """

    myQueue = util.PriorityQueue()
    visited = []

    startPos = problem.getStartState()
    node = (startPos, [], 0)

    #visited.append(startPos)

    #((startpos, [], 0), 0)
    myQueue.push(node, 0)       #push in 3 args: self, item, priority || node = item, 0 = priority
    while not myQueue.isEmpty():
        currentNode, path, priority = myQueue.pop()     #make new data current node to investigate

        if currentNode not in visited:      #dont append startnode at the top, otherwise it skips following code
            visited.append(currentNode)     #havent visited yet: add the node to visited list

            if problem.isGoalState(currentNode):
                return path                 #check if goal reached

            for successors, actions, cost in problem.getSuccessors(currentNode):    #check next nodes
                newPath = path + [actions]      #add successor path to path of current node
                totCost = priority + cost       #add cost to path's priority
                myQueue.push((successors, newPath, totCost), totCost)   #push new data back into queue




def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    myQueue = util.PriorityQueue()
    startPos = problem.getStartState()

    myQueue.push((startPos, [], 0), 0)
    while not myQueue.isEmpty():
        currentNode, path, priority = myQueue.pop()
        if currentNode not in visited:
            visited.append(currentNode)
            if problem.isGoalState(currentNode):
                return path
            for successors, actions, cost in problem.getSuccessors(currentNode):
                newCost = priority + cost
                addActions = path + [actions]
                newHeuristics = newCost + heuristic(successors, problem)   #newHeuristics is updated addActions
                myQueue.push((successors, addActions, newCost), newHeuristics)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
