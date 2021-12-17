import sys
import csv

# total arguments
n = len(sys.argv)

while n != 3:
    print("ERROR: Not enough or too many input arguments.\n")
    break

def getStateNames():
    with open('driving.csv') as f:
        reader = csv.reader(f, delimiter = ',')
        list_of_column_names = []
        for row in reader:
            list_of_column_names = [row]
            break
            
        return list_of_column_names[0]

""""
If -1, there is no path
If 0, then initialState == goalState
Else, there is a path
"""
def getDrivingDistance(fromStateLabel, toStateLabel):
    with open('driving.csv') as f:
        reader = csv.reader(f, delimiter = ',')
        populated_arr = []
        for row in reader:
            populated_arr.append(row)
            
        for r in range(len(populated_arr)):
            if(populated_arr[r][0] == fromStateLabel):
                for c in range(len(populated_arr[0])):
                    if(populated_arr[0][c] == toStateLabel):
                        return populated_arr[r][c]
        return '-1'
            
""""
If 0, then initialState == goalState
Else, there is a straight line path
h(n)
"""           
def getStraightLineDistance(fromStateLabel, goalStateLabel):
    with open('straightline.csv') as f:
        reader = csv.reader(f, delimiter = ',')
        populated_arr = []
        for row in reader:
            populated_arr.append(row)
            
        for r in range(len(populated_arr)):
            if(populated_arr[r][0] == fromStateLabel):
                for c in range(len(populated_arr[0])):
                    if(populated_arr[0][c] == goalStateLabel):
                        return populated_arr[r][c]
    return '0'
    
""""
Returns list of states with which state borders
"""
def stateBordersWith(state):
    with open('driving.csv') as f:
        reader = csv.reader(f, delimiter = ',')
        populated_arr = []
        statesBordered = []
        for row in reader:
            populated_arr.append(row)
            
        for r in range(len(populated_arr)):
            if(populated_arr[0][r] == state):
                for c in range(len(populated_arr[0])):
                    if(populated_arr[r][c] != '-1' and populated_arr[r][c] != '0' and c != 0):
                        statesBordered.append(populated_arr[0][c]) # [r][c] to get distance 
                        
    return statesBordered
    
     
""""
Use 
1. h(n) [Straight line] from goal state to any bordered state that selectedState borders
"""
def greedyBFS(initialStateLabel, goalStateLabel):
    least_straightline_from_goal = 1000000 # minimum
    totalDistance = 0
    
    distance = getDrivingDistance(initialStateLabel, goalStateLabel)
    pathway = initialStateLabel + ", " + goalStateLabel
    selectedState = initialStateLabel
    visitedStates = initialStateLabel
    savedState = ""
    count = 1
    
    # while there is no driving path from initialState to goalStateLabel
    # [UPDATE] and there is at least 1 path to other state [what if selectedState is Leaf node?]
    while(distance == '-1' and len(stateBordersWith(selectedState)) != 0):
        # get states bordered from selectedState
        list_of_possiblePaths = stateBordersWith(selectedState)
        
        # from the list of all bordered states
        for z in range(len(list_of_possiblePaths)):
            
            currState = list_of_possiblePaths[z] # get the state from list of states that have path from selectedState
            straightline_from_goalState_to_currState = getStraightLineDistance(goalStateLabel, currState) # h(n)
            
            # checks if h(n) < minimum
            # and if the currState has been classified as 'repeated' in visitedStates
            if ((int(straightline_from_goalState_to_currState) < least_straightline_from_goal) 
                and (not(currState in visitedStates))):
                
                least_straightline_from_goal = int(straightline_from_goalState_to_currState)
                savedState = currState # save the state
            
        totalDistance += int(getDrivingDistance(selectedState, savedState))
    
        least_straightline_from_goal = 1000000
        selectedState = savedState # selected state becomes the saved [curr] state
        savedState = ""
        visitedStates += ", " + selectedState # currState
        pathway = pathway[ : (4 * count)] + selectedState + ", " + pathway[(4 * count) : ]
        count += 1
        distance = getDrivingDistance(selectedState, goalStateLabel)
            
    totalDistance += int(getDrivingDistance(selectedState, goalStateLabel))
        
    print ("\nGreedy Best First:",
       "\nSolution path: ", pathway,
       "\nNumber of states on a path: ", count + 1,
        "\nPath cost: ", totalDistance, "\n")

""""
Use 
1. h(n) [Straight line] from goal state to any bordered state that selectedState borders
2. g(n) [Driving] from initial state to selectedState
3. hg = h(n)+g(n)
"""
def aStar(initialStateLabel, goalStateLabel):
    min_sum_of_hg = 1000000
    totalDistance = 0
    
    distance = getDrivingDistance(initialStateLabel, goalStateLabel)
    pathway = initialStateLabel + ", " + goalStateLabel
    selectedState = initialStateLabel
    visitedStates = initialStateLabel
    savedState = ""
    count = 1
    
    # while there is no driving path from initialState to goalStateLabel
    # [UPDATE] and there is at least 1 path to other state [what if selectedState is Leaf node?]
    while(distance == '-1' and len(stateBordersWith(selectedState)) != 0):
        # get states bordered from selectedState
        list_of_possiblePaths = stateBordersWith(selectedState)
        
        for i in range(len(list_of_possiblePaths)):
            
            currState = list_of_possiblePaths[i]  # get the state from list of states that have path from selectedState
            straightline_from_goalState_to_currState = getStraightLineDistance(goalStateLabel, currState) # h(n)
            driving_from_selectedState_to_currState = getDrivingDistance(selectedState, currState)        # g(n)
        
            # checks if h(n) + g(n) < minimum
            # and if the currState has been classified as 'repeated' in visitedStates
            if (((int(straightline_from_goalState_to_currState) + int(driving_from_selectedState_to_currState)) < min_sum_of_hg) 
                and (not(currState in visitedStates))):
                
                min_sum_of_hg = int(straightline_from_goalState_to_currState) + int(driving_from_selectedState_to_currState)
                savedState = currState # save the state
            
        totalDistance += int(getDrivingDistance(selectedState, savedState))
    
        min_sum_of_hg = 1000000
        selectedState = savedState # selected state becomes the saved [curr] state
        savedState = ""
        visitedStates += ", " + selectedState # currState
        pathway = pathway[ : (4 * count)] + selectedState + ", " + pathway[(4 * count) : ]
        count += 1
        distance = getDrivingDistance(selectedState, goalStateLabel)
            
    totalDistance += int(getDrivingDistance(selectedState, goalStateLabel))
        
    print ("A* Search:",
       "\nSolution path: ", pathway,
       "\nNumber of states on a path: ", count + 1,
        "\nPath cost: ", totalDistance, "\n")
    
          
initial = sys.argv[1]
goal = sys.argv[2]

exists = ( initial in getStateNames() ) and ( goal in getStateNames() )

if exists:
    print("Gaimakov, Timur, A20415319 solution:")
    print("Initial state: ", initial, "\nGoal state: ", goal)   
    greedyBFS(initial, goal)
    aStar(initial, goal)
else:
    print("Solution path: FAILURE: NO PATH FOUND")
    print("Number of states on a path: 0")
    print("Path cost: 0 miles")   
