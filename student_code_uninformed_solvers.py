from solver import *
from collections import deque


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #Set present node to visited
        self.visited[self.currentState] = True

        #Victory condition
        if self.currentState.state == self.victoryCondition:
            return True

        #iterate through all possible moves to determine weather victory state can be found
        for moves in self.gm.getMovables():
            self.gm.makeMove(moves)
            #Possible move stepState will be at one depth down of current state
            stepState = GameState(self.gm.getGameState(), self.currentState.depth+1, moves)
            self.currentState.children.append(stepState)
            stepState.parent = self.currentState
            #if visited, set indicator for next children to visit to next
            if stepState in self.visited.keys() and self.visited[stepState]:
                self.currentState.nextChildToVisit += 1
                self.gm.reverseMove(moves)
            else:
                self.currentState = stepState
                self.visited[stepState] = True
                return False
            
            

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.count = 0
        self.queue = deque()


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        output = []

        #Victory Condition            
        if self.currentState.state == self.victoryCondition:
            return True
            
        #Makes moves based on breath first search
        for moves in self.gm.getMovables():
            self.gm.makeMove(moves)
            #stepStates will occur at current depth + 1
            stepState = GameState(self.gm.getGameState(), self.currentState.depth + 1, moves)
            #sets children to parent node
            stepState.parent = self.currentState
            self.gm.reverseMove(moves)
            #enqueues all possible stepState children
            self.queue.append(stepState)
            self.currentState.children.append(stepState)
        
        #Counts the number of visited children out of the total
        while self.queue[self.count] in self.visited:
            self.count += 1
        
        #While there are still parents move back towards root
        while self.currentState.parent:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        #add potential children to queue if not visted via the algorithm
        while self.queue[self.count].parent:
            output.append(self.queue[self.count].requiredMovable)
            self.queue[self.count] = self.queue[self.count].parent

        #visit through children
        while len(output) != 0:
            self.gm.makeMove(output.pop())
            for child in self.currentState.children:
                if child.state == self.gm.getGameState():
                    self.visited[child] = True
                    self.currentState = child
        return False