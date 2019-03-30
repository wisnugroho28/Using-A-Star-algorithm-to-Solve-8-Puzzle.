from copy import deepcopy

case = [ [1 , 2 , 3],
			  [0 , 4 , 6],
			  [7 , 5 , 8]]
         
goal = [ [1 , 2 , 3],
      [4 , 5 , 6],
      [7 , 8 , 0]]

def getHammingValue(case):
    global goal
    hammingValue = 0
    for i in range(len(case)):												#Here, we are using a hamming value to define / state the position
        for j in range(len(case[i])):										#of the nodes in the array (puzzle board)
            if case[i][j] != goal[i][j] and goal[i][j] != 0:
                hammingValue += 1

    return hammingValue

def getManhattanDistance(case):
    manhattanSum = 0
    for i in range(len(case)):												#In this manhattan Distance function, we will find the shortest distance to the goal
        for j in range(len(case[i])):										
            value = case[i][j]
            if value != 0:
                targetX = (value - 1) / 3									#In this X and Y, we are matching the value of the goal and the value of the states
                targetY = (value - 1) % 3									#and check wether it is in the same array position, or not.
                deviationX = i - targetX									#if not, move the blank nodes again									
                deviationY = j - targetY
                if deviationX < 0:
                    deviationX *= -1
                elif deviationY < 0:
                    deviationY *= -1
                    
                manhattanSum += (deviationX + deviationY)

    return manhattanSum
    
    
class PriorityQueue(object): 
    def __init__(self): 
        self.queue = [] 
  
    # for checking if the queue is empty 
    def isEmpty(self): 
        return len(self.queue) == [] 
  
    # for inserting an element in the queue 
    def insert(self, data): 
        self.queue.append(data) 
  
    # for popping an element based on Priority 
    def delete(self): 
        try: 
            max = 0
            for i in range(len(self.queue)): 
                if self.queue[i].getPriorityValue() < self.queue[max].getPriorityValue(): 
                    max = i 
            item = deepcopy(self.queue[max]) 
            del self.queue[max] 
            return item
        except IndexError: 
            print() 
            exit()

class States:       
    
    def __init__(self,state,heuristic,dist,priorityValue,directionPath,lastIndex):
        self.heuristic = heuristic
        self.dist = dist
        self.priorityValue = priorityValue
        self.state = state
        self.directionPath = directionPath
        self.lastIndex = lastIndex
        self.parent = None
        
    def getPriorityValue(self):
        return self.priorityValue

    def getState(self):
        return self.state

    def getDist(self):
        return self.dist

    def getParent(self):
        return self.parent

    def setParent(self,parentState):
        self.parent = parentState

    def getPath(self):
        return self.directionPath

    def getLastIndex(self):
        return self.lastIndex

    def printList(self):
        print ("dist  : "),self.dist
        print ("state : "),self.state


def find_index_0(case):
    for i in range(len(case)):
        for j in range(len(case[i])):
            if case[i][j] == 0:
                return i,j

def swap(state,firstIndex,secondIndex):
    temp = state[firstIndex[0]][firstIndex[1]]
    state[firstIndex[0]][firstIndex[1]] = state[secondIndex[0]][secondIndex[1]]
    state[secondIndex[0]][secondIndex[1]] = temp
    return state

def printPath(goalState):

    if(goalState != None):
        printPath(goalState.getParent())
        print (goalState.getPath())
        print (goalState.getState())
        
    
    

if __name__ == '__main__':
    moves = [[-1,0],[1,0],[0,1],[0,-1]]
    currentHeuristic = getHammingValue(case) + getManhattanDistance(case)
    priorityValue = currentHeuristic
    lastZeroIndex = [-1,-1]
    currentState = States(case,currentHeuristic,0,priorityValue,"Start",lastZeroIndex)
    zero_index = find_index_0(currentState.getState())
    openList = PriorityQueue()
    closeList = []
    
    while True:


        if currentState.getState() == goal:
            print ("Found Solution!!")
            print ("Move = "),currentState.getDist()
            break
        
        for move in moves:
            predictedMove = zero_index[0] + move[0] , zero_index[1] + move[1]
            if predictedMove[0] >=0 and predictedMove[0] < 3 and predictedMove[1] >= 0 and predictedMove[1] < 3 and predictedMove != currentState.getLastIndex():
               
                originalState = deepcopy(currentState.getState())
                nextState = swap(originalState,predictedMove,zero_index)
                nextHeuristic = getHammingValue(nextState) + getManhattanDistance(nextState)
                nextDist = currentState.getDist() + 1
                nextPriority = nextHeuristic + nextDist
                lastZeroIndex = deepcopy(zero_index)

                if move == [-1,0]:
                    tracePath = "Up"
                elif move == [1,0]:
                    tracePath = "Down"
                elif move == [0,1]:
                    tracePath = "Right"
                elif move == [0,-1]:
                    tracePath = "Left"
                
                expandState = States(nextState,nextHeuristic,nextDist,nextPriority,tracePath,lastZeroIndex)
                expandState.setParent(currentState)
                openList.insert(expandState)

        currentState = openList.delete()
        zero_index = find_index_0(currentState.getState())
                        
        closeList.append(currentState)


    printPath(closeList.pop())