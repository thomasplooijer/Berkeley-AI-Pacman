# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        # see which legal move is the best one based on evaluation of surroundings
        # higher number/score is better move
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()         #pacman position after moving
        newFood = successorGameState.getFood()                  #remaining foods
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]  #number of moves that ghosts will remain scared

        "*** YOUR CODE HERE ***"

        #getPosition() gets the position of self. (ghost)
        ghostPos = [ghost.getPosition() for ghost in newGhostStates]
        #print newPos
        #print ghostPos

        #get manhattandistance to nearest ghost || manhattanDistance(ghostPos, currentPos)
        #the closer the ghost, the worse the scorenumber
        nearestGhost = min([manhattanDistance(ghostPos[0][:], newPos)])
        #print nearestGhost
        ghostScore = 0


        #if len(newScaredTimes) == 0:
         #   print newScaredTimes
         #   ghostScore += 10

        if nearestGhost > 15:
            ghostScore = 6
        elif nearestGhost >= 3 and nearestGhost <= 15:
            ghostScore = 2
        else:
            ghostScore = 0.2

        foods = newFood.asList()
        #print foods
        #food[0][:]

        foodScore = 0
        #as long as there are foods
        if len(foods) != 0:
            #look for closest food in foodlist
            nearestFood = min([manhattanDistance(newPos, food)] for food in newFood.asList())
            #print nearestFood

            #the closer the food, the higher the scorenumber
            if nearestFood[0] >= 12:
                foodScore = 0.2
            elif nearestFood[0] < 12 and nearestFood[0] >= 5:
                foodScore = 1
            else:
                nearestFood[0] < 5
                foodScore = 5

        #print ghostScore + foodScore
        #higher numbers are better
        return successorGameState.getScore() + ghostScore + foodScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        #this part gives (gamestate, agents, depth) to minimax()
        #is the game over?
        miniMaxValues = []
        legalAct = gameState.getLegalActions(0)
        #print legalAct
        for actions in legalAct:
            #calculates miniMax values for agent 0 (pacman) depending on its legal following actions, spooks and how far we want to look ahead
            value = self.miniMax(gameState.generateSuccessor(0, actions), 1, 0)
            miniMaxValues.append((value, actions))
        #print miniMaxValues
        return max(miniMaxValues)[1]

    #my miniMax function
    def miniMax(self, gameState, agent, depth):
        #increase depth
        if agent >= gameState.getNumAgents():
            depth += 1
            agent = 0

        if depth == self.depth:
            #if reached maximum depth, return evaluated score
            return self.evaluationFunction(gameState)

        #are there any legal actions?
        legalAct = gameState.getLegalActions(agent)
        if not legalAct:
            #return evaluated score of current gamestate (pacman, legalactions)
            return self.evaluationFunction(gameState)

        #this is the meat of the function: pacman is maximizing, spooks are minimizing
        miniMaxValues = []
        #minimax for pacman
        if agent == 0:
            #for each child node
            for actions in legalAct:
                value = self.miniMax(gameState.generateSuccessor(agent, actions), agent+1, depth)
                #print("values are:")
                #print value
                miniMaxValues.append((value,actions))
            #print("chosen value:")
            #print max(miniMaxValues)[0]
            return max(miniMaxValues)[0]
        #minimax for other agents/spooks
        else:
            #for each child node
            for actions in legalAct:
                value = self.miniMax(gameState.generateSuccessor(agent, actions), agent+1, depth)
                miniMaxValues.append((value, actions))
            return min(miniMaxValues)[0]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** WORKING ON CODE HERE ***"
#this part gives (gamestate, agents, depth) to minimax()
        alpha = float('-inf')     #positive infinity
        beta = float('inf')   #negative infinity

        #is the game over?
        #miniMaxValues = []
        v = (float('-inf'), 'none')
        legalAct = gameState.getLegalActions(0)
        #print legalAct
        for actions in legalAct:
            #calculates miniMax values for agent 0 (pacman) depending on its legal following actions, spooks and how far we want to look ahead
            #value = self.AlphaBeta(gameState.generateSuccessor(0, actions), 1, 0, alpha, beta)
            v = max(v, (self.AlphaBeta(gameState.generateSuccessor(0, actions), 1, 0, alpha, beta), actions))
            if v[0] > beta:
                return v[1]
            alpha = max(v[0], alpha)
        return v[1]

    #my miniMax function
    def AlphaBeta(self, gameState, agent, depth, alpha, beta):
        #increase depth
        if agent >= gameState.getNumAgents():
            depth += 1
            agent = 0

        if depth == self.depth:
            #if reached maximum depth, return evaluated score
            return self.evaluationFunction(gameState)

        #are there any legal actions?
        legalAct = gameState.getLegalActions(agent)
        if not legalAct:
            #return evaluated score of current gamestate (pacman, legalactions)
            return self.evaluationFunction(gameState)

        #this is the meat of the function: pacman is maximizing, spooks are minimizing
        miniMaxValues = []
        #minimax for pacman
        if agent == 0:
            maxEval = float('-inf')
            #for each child node
            for actions in legalAct:
                #value = self.AlphaBeta(gameState.generateSuccessor(agent, actions), agent+1, depth, alpha, beta)
                maxEval = max(self.AlphaBeta(gameState.generateSuccessor(agent, actions), agent+1, depth, alpha, beta), maxEval)
                if maxEval > beta:
                    return maxEval
                alpha = max(alpha, maxEval)
            return maxEval

        #minimax for other agents/spooks
        else:
            minEval = float('inf')
            #for each child node
            for actions in legalAct:
                #value = self.AlphaBeta(gameState.generateSuccessor(agent, actions), agent+1, depth, alpha, beta)
                minEval = min(self.AlphaBeta(gameState.generateSuccessor(agent, actions), agent+1, depth, alpha, beta), minEval)
                if minEval < alpha:
                    return minEval
                beta = min(beta, minEval)
            return minEval

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

